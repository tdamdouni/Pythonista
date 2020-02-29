# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2009, 2013, Oracle and/or its affiliates. All rights reserved.

# MySQL Connector/Python is licensed under the terms of the GPLv2
# <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>, like most
# MySQL Connectors. There are special exceptions to the terms and
# conditions of the GPLv2 as it is applied to this software, see the
# FOSS License Exception
# <http://www.mysql.com/about/legal/licensing/foss-exception.html>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

"""Implementing communication with MySQL servers.
"""

import os
import time
import re

from network import (MySQLUnixSocket, MySQLTCPSocket)
from constants import (ClientFlag, ServerCmd, CharacterSet,
    ServerFlag, flag_is_set, ShutdownType)
from conversion import MySQLConverter
from protocol import MySQLProtocol
import errors
from utils import (int4store, int1store)
from cursor import (CursorBase, MySQLCursor, MySQLCursorRaw,
    MySQLCursorBuffered, MySQLCursorBufferedRaw)

DEFAULT_CONFIGURATION = {
    'database': None,
    'user': '',
    'password': '',
    'host': '127.0.0.1',
    'port': 3306,
    'unix_socket': None,
    'use_unicode': True,
    'charset': 'utf8',
    'collation': None,
    'autocommit': False,
    'time_zone': None,
    'sql_mode': None,
    'get_warnings': False,
    'raise_on_warnings': False,
    'connection_timeout': None,
    'client_flags': 0,
    'buffered': False,
    'raw': False,
    'ssl_ca': None,
    'ssl_cert': None,
    'ssl_key': None,
    'ssl_verify_cert': False,
    'passwd': None,
    'db': None,
    'connect_timeout': None,
    'dsn': None,
    'force_ipv6': False,
}

class MySQLConnection(object):
    """Connection to a MySQL Server"""
    def __init__(self, **kwargs):
        self._protocol = None
        self._socket = None
        self._handshake = None
        self._server_version = None
        self.converter = None
        self._converter_class = None

        self._client_flags = ClientFlag.get_default()
        self._charset_id = 33
        self._sql_mode = None
        self._time_zone = None
        self._autocommit = False

        self._user = ''
        self._password = ''
        self._database = ''
        self._host = '127.0.0.1'
        self._port = 3306
        self._unix_socket = None
        self._client_host = ''
        self._client_port = 0
        self._ssl = {}
        self._force_ipv6 = False

        self._use_unicode = True
        self._get_warnings = False
        self._raise_on_warnings = False
        self._connection_timeout = None
        self._buffered = False
        self._unread_result = False
        self._have_next_result = False
        self._raw = False

        if len(kwargs) > 0:
            self.connect(**kwargs)

    def _get_self(self):
        """Return self for weakref.proxy
        
        This method is used when the original object is needed when using
        weakref.proxy.
        """
        return self

    def _do_handshake(self):
        """Get the handshake from the MySQL server"""
        packet = self._socket.recv()
        if packet[4] == '\xff':
            raise errors.get_exception(packet)

        try:
            handshake = self._protocol.parse_handshake(packet)
        except Exception as err:
            raise errors.InterfaceError('Failed parsing handshake; %s' % err)

        regex_ver = re.compile("^(\d{1,2})\.(\d{1,2})\.(\d{1,3})(.*)")
        match = regex_ver.match(handshake['server_version_original'])
        if not match:
            raise errors.InterfaceError("Failed parsing MySQL version")

        version = tuple([ int(v) for v in match.groups()[0:3]])
        if version < (4, 1):
            raise errors.InterfaceError(
                "MySQL Version '%s' is not supported." % \
                handshake['server_version_original'])

        self._handshake = handshake
        self._server_version = version

    def _do_auth(self, username=None, password=None, database=None,
                 client_flags=0, charset=33, ssl_options=None):
        """Authenticate with the MySQL server
        """
        if client_flags & ClientFlag.SSL and ssl_options:
            packet = self._protocol.make_auth_ssl(charset=charset,
                                                  client_flags=client_flags)
            self._socket.send(packet)
            self._socket.switch_to_ssl(**ssl_options)

        packet = self._protocol.make_auth(
            seed=self._handshake['scramble'],
            username=username, password=password, database=database,
            charset=charset, client_flags=client_flags)
        self._socket.send(packet)
        packet = self._socket.recv()

        if packet[4] == '\xfe':
            raise errors.NotSupportedError(
              "Authentication with old (insecure) passwords "\
              "is not supported. For more information, lookup "\
              "Password Hashing in the latest MySQL manual")
        elif packet[4] == '\xff':
            raise errors.get_exception(packet)

        try:
            if (not (client_flags & ClientFlag.CONNECT_WITH_DB)
                and database):
                self.cmd_init_db(database)
        except:
            raise

        return True

    def config(self, **kwargs):
        """Configure the MySQL Connection

        This method allows you to configure the MySQLConnection instance.

        Raises on errors.
        """
        config = kwargs.copy()
        if 'dsn' in config:
            raise errors.NotSupportedError("Data source name is not supported")

        # Configure how we handle MySQL warnings
        try:
            self.get_warnings = config['get_warnings']
            del config['get_warnings']
        except KeyError:
            pass # Leave what was set or default
        try:
            self.raise_on_warnings = config['raise_on_warnings']
            del config['raise_on_warnings']
        except KeyError:
            pass # Leave what was set or default

        # Configure client flags
        try:
            default = ClientFlag.get_default()
            self.set_client_flags(config['client_flags'] or default)
            del config['client_flags']
        except KeyError:
            pass # Missing client_flags-argument is OK

        # Configure character set and collation
        if ('charset' in config or 'collation' in config):
            try:
                charset = config['charset']
                del config['charset']
            except KeyError:
                charset = None
            try:
                collation = config['collation']
                del config['collation']
            except KeyError:
                collation = None
            self._charset_id = CharacterSet.get_charset_info(charset,
                                    collation)[0]

        # Compatible configuration with other drivers
        compat_map = [
            # (<other driver argument>,<translates to>)
            ('db','database'),
            ('passwd','password'),
            ('connect_timeout','connection_timeout'),
        ]
        for compat, translate in compat_map:
            try:
                if translate not in config:
                    config[translate] = config[compat]
                del config[compat]
            except KeyError:
                pass # Missing compat argument is OK

        # Configure login information
        if ('user' in config or 'password' in config):
            try:
                user = config['user']
                del config['user']
            except KeyError:
                user = self._user
            try:
                password = config['password']
                del config['password']
            except KeyError:
                password = self._password
            self.set_login(user, password)

        # Check network locations
        try:
            self._port = int(config['port'])
            del config['port']
        except KeyError:
            pass # Missing port argument is OK
        except ValueError:
            raise errors.InterfaceError(
                "TCP/IP port number should be an integer")

        # Other configuration
        set_ssl_flag = False
        for key, value in config.items():
            try:
                DEFAULT_CONFIGURATION[key]
            except KeyError:
                raise AttributeError("Unsupported argument '%s'" % key)
            # SSL Configuration
            if key == 'ssl_verify_cert':
                set_ssl_flag = True
                self._ssl.update({'verify_cert': value})
            elif key.startswith('ssl_') and value:
                set_ssl_flag = True
                self._ssl.update({key.replace('ssl_', ''): value})
            else:
                attribute = '_' + key
                try:
                    setattr(self, attribute, value.strip())
                except AttributeError:
                    setattr(self, attribute, value)

        if set_ssl_flag:
            if 'verify_cert' not in self._ssl:
                self._ssl['verify_cert'] = \
                    DEFAULT_CONFIGURATION['ssl_verify_cert']
            required_keys = set(['ca', 'cert', 'key'])
            diff = list(required_keys - set(self._ssl.keys()))
            if diff:
                missing_attrs = [ "ssl_" + val for val in diff ]
                raise AttributeError("Missing SSL argument(s): %s" % (
                    ', '.join(missing_attrs)))
            self.set_client_flags([ClientFlag.SSL])

    def _get_connection(self):
        """Get connection based on configuration

        This method will return the appropriated connection object using
        the connection parameters.

        Returns subclass of MySQLBaseSocket.
        """
        conn = None
        if self.unix_socket and os.name != 'nt':
            conn = MySQLUnixSocket(unix_socket=self.unix_socket)
        else:
            conn = MySQLTCPSocket(host=self.server_host,
                                  port=self.server_port,
                                  force_ipv6=self._force_ipv6)
        conn.set_connection_timeout(self._connection_timeout)
        return conn

    def _open_connection(self):
        """Open the connection to the MySQL server

        This method sets up and opens the connection to the MySQL server.
        """
        self._socket = self._get_connection()
        self._socket.open_connection()
        self._do_handshake()
        self._do_auth(self._user, self._password,
                      self._database, self._client_flags, self._charset_id,
                      self._ssl)
        self.set_converter_class(MySQLConverter)
        if self._client_flags & ClientFlag.COMPRESS:
            self._socket.recv = self._socket.recv_compressed
            self._socket.send = self._socket.send_compressed

    def _post_connection(self):
        """Executes commands after connection has been established

        This method executes commands after the connection has been
        established. Some setting like autocommit, character set, and SQL mode
        are set using this method.
        """
        self.set_charset_collation(charset=self._charset_id)
        self.autocommit = self._autocommit
        if self._time_zone:
            self.time_zone = self._time_zone
        if self._sql_mode:
            self.sql_mode = self._sql_mode

    def connect(self, **kwargs):
        """Connect to the MySQL server

        This method sets up the connection to the MySQL server. If no
        arguments are given, it will use the already configured or default
        values.
        """
        if len(kwargs) > 0:
            self.config(**kwargs)

        self._protocol = MySQLProtocol()

        self.disconnect()
        self._open_connection()
        self._post_connection()

    def disconnect(self):
        """Disconnect from the MySQL server
        """
        if not self._socket:
            return

        try:
            self.cmd_quit()
            self._socket.close_connection()
        except errors.Error:
            pass # Getting an exception would mean we are disconnected.
    close = disconnect

    def _send_cmd(self, command, argument=None, packet_number=0):
        """Send a command to the MySQL server

        This method sends a command with an optional argument.

        Returns a MySQL packet
        """
        if self.unread_result:
            raise errors.InternalError("Unread result found.")
        
        try:
            self._socket.send(self._protocol.make_command(command, argument),
                              packet_number)
        except AttributeError:
            raise errors.OperationalError("MySQL Connection not available.")

        return self._socket.recv()

    def _send_data(self, fp, send_empty_packet=False):
        """Send data to the MySQL server

        This method accepts a file-like object and sends its data
        as is to the MySQL server. If the send_empty_packet is
        True, it will send an extra empty package (for example
        when using LOAD LOCAL DATA INFILE).

        Returns a MySQL packet.
        """
        if self.unread_result:
            raise errors.InternalError("Unread result found.")

        if not hasattr(fp, 'read'):
            raise ValueError("expecting a file-like object")

        try:
            buf = fp.read(4096)
            while buf:
                self._socket.send(buf)
                buf = fp.read(4096)
        except AttributeError:
            raise errors.OperationalError("MySQL Connection not available.")

        if send_empty_packet:
            try:
                self._socket.send('')
            except AttributeError:
                raise errors.OperationalError(
                    "MySQL Connection not available.")

        return self._socket.recv()

    def _toggle_have_next_result(self, flags):
        """Toggle whether there more results
        
        This method checks the whether MORE_RESULTS_EXISTS is set in flags.
        """
        if flag_is_set(ServerFlag.MORE_RESULTS_EXISTS, flags):
            self._have_next_result = True
        else:
            self._have_next_result = False

    def _handle_ok(self, packet):
        """Handle a MySQL OK packet

        This method handles a MySQL OK packet. When the packet is found to
        be an Error packet, an error will be raised. If the packet is neither
        an OK or an Error packet, errors.InterfaceError will be raised.

        Returns a dict()
        """
        if packet[4] == '\x00':
            ok = self._protocol.parse_ok(packet)
            self._toggle_have_next_result(ok['server_status'])
            return ok
        elif packet[4] == '\xff':
            raise errors.get_exception(packet)
        raise errors.InterfaceError('Expected OK packet')

    def _handle_eof(self, packet):
        """Handle a MySQL EOF packet

        This method handles a MySQL EOF packet. When the packet is found to
        be an Error packet, an error will be raised. If the packet is neither
        and OK or an Error packet, errors.InterfaceError will be raised.

        Returns a dict()
        """
        if packet[4] == '\xfe':
            eof = self._protocol.parse_eof(packet)
            self._toggle_have_next_result(eof['status_flag'])
            return eof
        elif packet[4] == '\xff':
            raise errors.get_exception(packet)
        raise errors.InterfaceError('Expected EOF packet')

    def _handle_load_data_infile(self, filename):
        """Handle a LOAD DATA INFILE LOCAL request"""
        try:
            fp = open(filename, 'rb')
        except IOError:
            # Send a empty packet to cancel the operation
            try:
                self._socket.send('')
            except AttributeError:
                raise errors.OperationalError(
                    "MySQL Connection not available.")
            raise errors.InterfaceError("File '%s' could not be read" %
                filename)

        return self._handle_ok(self._send_data(fp, send_empty_packet=True))

    def _handle_result(self, packet):
        """Handle a MySQL Result

        This method handles a MySQL result, for example, after sending the
        query command. OK and EOF packets will be handled and returned. If
        the packet is an Error packet, an errors.Error-exception will be
        raised.

        The dictionary returned of:
        - columns: column information
        - eof: the EOF-packet information

        Returns a dict()
        """
        if not packet or len(packet) < 4:
            raise errors.InterfaceError('Empty response')
        elif packet[4] == '\x00':
            return self._handle_ok(packet)
        elif packet[4] == '\xfb':
            return self._handle_load_data_infile(packet[5:])
        elif packet[4] == '\xfe':
            return self._handle_eof(packet)
        elif packet[4] == '\xff':
            raise errors.get_exception(packet)

        # We have a text result set
        column_count = self._protocol.parse_column_count(packet)
        if not column_count or not isinstance(column_count, int):
            raise errors.InterfaceError('Illegal result set.')

        columns = [None,]*column_count
        for i in xrange(0, column_count):
            columns[i] = self._protocol.parse_column(self._socket.recv())

        eof = self._handle_eof(self._socket.recv())
        self.unread_result = True
        return {'columns': columns, 'eof': eof}

    def get_rows(self, count=None):
        """Get all rows returned by the MySQL server

        This method gets all rows returned by the MySQL server after sending,
        for example, the query command. The result is a tuple consisting of
        a list of rows and the EOF packet.

        Returns a tuple()
        """
        if not self.unread_result:
            raise errors.InternalError("No result set available.")
        
        rows = self._protocol.read_text_result(self._socket, count)
        if rows[-1] is not None:
            self._toggle_have_next_result(rows[-1]['status_flag'])
            self.unread_result = False
        
        return rows

    def get_row(self):
        """Get the next rows returned by the MySQL server

        This method gets one row from the result set after sending, for
        example, the query command. The result is a tuple consisting of the
        row and the EOF packet.
        If no row was available in the result set, the row data will be None.

        Returns a tuple.
        """
        (rows, eof) = self.get_rows(count=1)
        if len(rows):
            return (rows[0], eof)
        return (None, eof)

    def cmd_init_db(self, database):
        """Change the current database

        This method changes the current (default) database by sending the
        INIT_DB command. The result is a dictionary containing the OK packet
        information.

        Returns a dict()
        """
        return self._handle_ok(self._send_cmd(ServerCmd.INIT_DB, database))

    def cmd_query(self, statement):
        """Send a statement to the MySQL server

        This method sends the given statement to the MySQL server and
        returns a result. If you need to send multiple statements, you
        have to use the cmd_query_iter() method.

        The returned dictionary contains information depending on what kind
        of query was executed. If the query is a SELECT statement, the result
        will contain information about columns. Other statements will return
        a dictionary containing an OK or EOF packet.

        Errors received from the MySQL server will be raised as exceptions.
        An InterfaceError is raised when multiple results were found.

        Returns a dictionary.
        """
        result = self._handle_result(self._send_cmd(ServerCmd.QUERY,
                                                    statement))
        
        if self._have_next_result:
             raise errors.InterfaceError(
                'Use cmd_query_iter for statements with multiple queries.')
        return result

    def cmd_query_iter(self, statements):
        """Send one or more statements to the MySQL server

        Similar to the cmd_query method, but instead returns a generator
        object to iterate through results. It sends the statements to the
        MySQL server and through the iterator you can get the results.
        
        statement = 'SELECT 1; INSERT INTO t1 VALUES (); SELECT 2'
        for result in cnx.cmd_query(statement, iterate=True):
            if 'columns' in result:
                columns = result['columns']
                rows = cnx.get_rows()
            else:
                # do something useful with INSERT result

        Returns a generator.
        """
        # Handle the first query result
        yield self._handle_result(self._send_cmd(ServerCmd.QUERY, statements))
        
        # Handle next results, if any
        while self._have_next_result:
            if self.unread_result:
                raise errors.InternalError("Unread result found.")
            else:
                result = self._handle_result(self._socket.recv())
            yield result

    def cmd_refresh(self, options):
        """Send the Refresh command to the MySQL server

        This method sends the Refresh command to the MySQL server. The options
        argument should be a bitwise value using contants.RefreshOption.
        Usage example:
         RefreshOption = mysql.connector.RefreshOption
         refresh = RefreshOption.LOG | RefreshOption.THREADS
         cnx.cmd_refresh(refresh)

        The result is a dictionary with the OK packat information.

        Returns a dict()
        """
        return self._handle_ok(
            self._send_cmd(ServerCmd.REFRESH, int4store(options)))

    def cmd_quit(self):
        """Close the current connection with the server

        This method sends the QUIT command to the MySQL server, closing the
        current connection. Since the no response can be returned to the
        client, cmd_quit() will return the packet it send.

        Returns a str()
        """
        if self.unread_result:
            raise errors.InternalError("Unread result found.")

        packet = self._protocol.make_command(ServerCmd.QUIT)
        self._socket.send(packet, 0)
        return packet

    def cmd_shutdown(self, shutdown_type=None):
        """Shut down the MySQL Server

        This method sends the SHUTDOWN command to the MySQL server and is only
        possible if the current user has SUPER privileges. The result is a
        dictionary containing the OK packet information.

        Note: Most applications and scripts do not the SUPER privilege.

        Returns a dict()
        """
        atype = None
        if shutdown_type:
            if not ShutdownType.get_info(shutdown_type):
                raise errors.InterfaceError("Invalid shutdown type")
            atype = int1store(shutdown_type)
        return self._handle_eof(self._send_cmd(ServerCmd.SHUTDOWN, atype))

    def cmd_statistics(self):
        """Send the statistics command to the MySQL Server

        This method sends the STATISTICS command to the MySQL server. The
        result is a dictionary with various statistical information.

        Returns a dict()
        """
        if self.unread_result:
            raise errors.InternalError("Unread result found.")

        packet = self._protocol.make_command(ServerCmd.STATISTICS)
        self._socket.send(packet, 0)
        return self._protocol.parse_statistics(self._socket.recv())

    def cmd_process_info(self):
        """Get the process list of the MySQL Server

        This method is a placeholder to notify that the PROCESS_INFO command
        is not supported by raising the NotSupportedError. The command
        "SHOW PROCESSLIST" should be send using the cmd_query()-method or
        using the INFORMATION_SCHEMA database.

        Raises NotSupportedError exception
        """
        raise errors.NotSupportedError(
            "Not implemented. Use SHOW PROCESSLIST or INFORMATION_SCHEMA")

    def cmd_process_kill(self, mysql_pid):
        """Kill a MySQL process

        This method send the PROCESS_KILL command to the server along with
        the process ID. The result is a dictionary with the OK packet
        information.

        Returns a dict()
        """
        return self._handle_ok(
            self._send_cmd(ServerCmd.PROCESS_KILL, int4store(mysql_pid)))

    def cmd_debug(self):
        """Send the DEBUG command

        This method sends the DEBUG command to the MySQL server, which
        requires the MySQL user to have SUPER privilege. The output will go
        to the MySQL server error log and the result of this method is a
        dictionary with EOF packet information.

        Returns a dict()
        """
        return self._handle_eof(self._send_cmd(ServerCmd.DEBUG))

    def cmd_ping(self):
        """Send the PING command

        This method sends the PING command to the MySQL server. It is used to
        check if the the connection is still valid. The result of this
        method is dictionary with OK packet information.

        Returns a dict()
        """
        return self._handle_ok(self._send_cmd(ServerCmd.PING))

    def cmd_change_user(self, username='', password='', database='',
                        charset=33):
        """Change the current logged in user

        This method allows to change the current logged in user information.
        The result is a dictionary with OK packet information.

        Returns a dict()
        """
        if self.unread_result:
            raise errors.InternalError("Unread result found.")

        packet = self._protocol.make_change_user(
            seed=self._handshake['scramble'],
            username=username, password=password, database=database,
            charset=charset, client_flags=self._client_flags)
        self._socket.send(packet, 0)
        return self._handle_ok(self._socket.recv())

    def is_connected(self):
        """Reports whether the connection to MySQL Server is available

        This method checks whether the connection to MySQL is available.
        It is similar to ping(), but unlike the ping()-method, either True
        or False is returned and no exception is raised.

        Returns True or False.
        """
        try:
            self.cmd_ping()
        except errors.Error:
            return False # This method does not raise
        return True

    def reconnect(self, attempts=1, delay=0):
        """Attempt to reconnect to the MySQL server

        The argument attempts should be the number of times a reconnect
        is tried. The delay argument is the number of seconds to wait between
        each retry.

        You may want to set the number of attempts higher and use delay when
        you expect the MySQL server to be down for maintenance or when you
        expect the network to be temporary unavailable.

        Raises InterfaceError on errors.
        """
        counter = 0
        while counter != attempts:
            counter = counter + 1
            try:
                self.disconnect()
                self.connect()
            except Exception as err:
                if counter == attempts:
                    raise errors.InterfaceError("Can not reconnect to MySQL "
                                                "after %d attempt(s): %s" % (
                                                attempts, str(err)))
            if delay > 0:
                time.sleep(delay)

    def ping(self, reconnect=False, attempts=1, delay=0):
        """Check availability to the MySQL server

        When reconnect is set to True, one or more attempts are made to try
        to reconnect to the MySQL server using the reconnect()-method.

        delay is the number of seconds to wait between each retry.

        When the connection is not available, an InterfaceError is raised. Use
        the is_connected()-method if you just want to check the connection
        without raising an error.

        Raises InterfaceError on errors.
        """
        try:
            self.cmd_ping()
        except errors.Error:
            if reconnect:
                self.reconnect(attempts=attempts, delay=delay)
            else:
                raise errors.InterfaceError("Connection to MySQL is"
                                            " not available.")

    def set_converter_class(self, convclass):
        """
        Set the converter class to be used. This should be a class overloading
        methods and members of conversion.MySQLConverter.
        """
        charset_name = CharacterSet.get_info(self._charset_id)[0]
        self._converter_class = convclass
        self.converter = convclass(charset_name, self._use_unicode)

    def get_server_version(self):
        """Get the MySQL version

        This method returns the MySQL server version as a tuple. If not
        perviously connected, it will return None.

        Returns a tuple or None.
        """
        return self._server_version

    def get_server_info(self):
        """Get the original MySQL version information

        This method returns the original MySQL server as text. If not
        previously connected, it will return None.

        Returns a string or None.
        """
        try:
            return self._handshake['server_version_original']
        except (TypeError, KeyError):
            return None

    @property
    def connection_id(self):
        """MySQL connection ID"""
        try:
            return self._handshake['server_threadid']
        except KeyError:
            return None

    def set_login(self, username=None, password=None):
        """Set login information for MySQL

        Set the username and/or password for the user connecting to
        the MySQL Server.
        """
        if username is not None:
            self._user = username.strip()
        else:
            self._user = ''
        if password is not None:
            self._password = password.strip()
        else:
            self._password = ''

    def set_unicode(self, value=True):
        """Toggle unicode mode

        Set whether we return string fields as unicode or not.
        Default is True.
        """
        self._use_unicode = value
        if self.converter:
            self.converter.set_unicode(value)

    def set_charset_collation(self, charset=None, collation=None):
        """Sets the character set and collation for the current connection

        This method sets the character set and collation to be used for
        the current connection. The charset argument can be either the
        name of a character set as a string, or the numerical equivalent
        as defined in constants.CharacterSet.

        When the collation is not given, the default will be looked up and
        used.

        For example, the following will set the collation for the latin1
        character set to latin1_general_ci:

           set_charset('latin1','latin1_general_ci')

        """
        if charset:
            if isinstance(charset, int):
                self._charset_id = charset
                (charset_name, collation_name) = CharacterSet.get_info(
                    self._charset_id)
            elif isinstance(charset, str):
                (self._charset_id, charset_name, collation_name) = \
                    CharacterSet.get_charset_info(charset, collation)
            else:
                raise ValueError(
                    "charset should be either integer, string or None")
        elif collation:
            (self._charset_id, charset_name, collation_name) = \
                    CharacterSet.get_charset_info(collation=collation)

        self._execute_query("SET NAMES '%s' COLLATE '%s'" % (
            charset_name, collation_name))
        self.converter.set_charset(charset_name)

    @property
    def charset(self):
        """Returns the character set for current connection

        This property returns the character set name of the current connection.
        Note that the value returned is based on what is previously set by
        the set_charset_collation().

        Returns a string.
        """
        return CharacterSet.get_info(self._charset_id)[0]

    @property
    def collation(self):
        """Returns the collation for current connection

        This property returns the collation name of the current connection.
        Note that the value returned is based on what is previously set by
        the set_charset_collation().

        Returns a string.
        """
        return CharacterSet.get_charset_info(self._charset_id)[2]

    def set_client_flags(self, flags):
        """Set the client flags

        The flags-argument can be either an int or a list (or tuple) of
        ClientFlag-values. If it is an integer, it will set client_flags
        to flags as is.
        If flags is a list (or tuple), each flag will be set or unset
        when it's negative.

        set_client_flags([ClientFlag.FOUND_ROWS,-ClientFlag.LONG_FLAG])
        
        Raises ProgrammingError when the flags argument is not a set or
        an integer bigger than 0.

        Returns self._client_flags
        """
        if isinstance(flags, int) and flags > 0:
            self._client_flags = flags
        elif isinstance(flags, (tuple, list)):
            for flag in flags:
                if flag < 0:
                    self._client_flags &= ~abs(flag)
                else:
                    self._client_flags |= flag
        else:
            raise errors.ProgrammingError(
                "set_client_flags expect int (>0) or set")

        return self._client_flags

    def isset_client_flag(self, flag):
        """Check if a client flag is set"""
        if (self._client_flags & flag) > 0:
            return True
        return False

    @property
    def user(self):
        """User used while connecting to MySQL"""
        return self._user

    @property
    def server_host(self):
        """MySQL server IP address or name"""
        return self._host

    @property
    def server_port(self):
        "MySQL server TCP/IP port"
        return self._port

    @property
    def unix_socket(self):
        "MySQL Unix socket file location"
        return self._unix_socket

    def _set_unread_result(self, toggle):
        """Set whether there is an unread resultself._port

        This method is used by cursors to let other cursors know there is
        still a result set that needs to be retrieved.

        Raises ValueError on errors.
        """
        if not isinstance(toggle, bool):
            raise ValueError("Expected a boolean type")
        self._unread_result = toggle

    def _get_unread_result(self):
        """Get whether there is an unread result

        This method is used by cursors to check whether another cursor still
        needs to retrieve its result set.

        Returns True, or False when there is no unread result.
        """
        return self._unread_result

    unread_result = property(_get_unread_result, _set_unread_result,
        doc="Unread result for this MySQL connection")

    def set_database(self, value):
        """Set the current database"""
        self.cmd_query("USE %s" % value)
    def get_database(self):
        """Get the current database"""
        return self._info_query("SELECT DATABASE()")[0]
    database = property(get_database, set_database,
        doc="Current database")

    def set_time_zone(self, value):
        """Set the time zone"""
        self.cmd_query("SET @@session.time_zone = '%s'" % value)
        self._time_zone = value
    def get_time_zone(self):
        """Get the current time zone"""
        return self._info_query("SELECT @@session.time_zone")[0]
    time_zone = property(get_time_zone, set_time_zone,
        doc="time_zone value for current MySQL session")

    def set_sql_mode(self, value):
        """Set the SQL mode

        This method sets the SQL Mode for the current connection. The value
        argument can be either a string with comma sepearate mode names, or
        a sequence of mode names.

        It is good practice to use the constants class SQLMode:
          from mysql.connector.constants import SQLMode 
          cnx.sql_mode = [SQLMode.NO_ZERO_DATE, SQLMode.REAL_AS_FLOAT]
        """
        if isinstance(value, (list, tuple)):
            value = ','.join(value)
        self.cmd_query("SET @@session.sql_mode = '%s'" % value)
        self._sql_mode = value
    def get_sql_mode(self):
        """Get the SQL mode"""
        return self._info_query("SELECT @@session.sql_mode")[0]
    sql_mode = property(get_sql_mode, set_sql_mode,
        doc="sql_mode value for current MySQL session")

    def set_autocommit(self, value):
        """Toggle autocommit"""
        if value:
            switch = 'ON'
        else:
            switch = 'OFF'
        self._execute_query("SET @@session.autocommit = %s" % switch)
    def get_autocommit(self):
        """Get whether autocommit is on or off"""
        value = self._info_query("SELECT @@session.autocommit")[0]
        if value == 1:
            return True
        return False
    autocommit = property(get_autocommit, set_autocommit,
        doc="autocommit value for current MySQL session")

    def _set_getwarnings(self, toggle):
        """Set whether warnings should be automatically retrieved

        The toggle-argument must be a boolean. When True, cursors for this
        connection will retrieve information about warnings (if any).

        Raises ValueError on error.
        """
        if not isinstance(toggle, bool):
            raise ValueError("Expected a boolean type")
        self._get_warnings = toggle

    def _get_getwarnings(self):
        """Get whether this connection retrieves warnings automatically

        This method returns whether this connection retrieves warnings
        automatically.

        Returns True, or False when warnings are not retrieved.
        """
        return self._get_warnings
    get_warnings = property(_get_getwarnings, _set_getwarnings,
                            doc="Toggle and check wheter to retrieve "\
                                "warnings automatically")

    def _set_raise_on_warnings(self, toggle):
        """Set whether warnings raise an error

        The toggle-argument must be a boolean. When True, cursors for this
        connection will raise an error when MySQL reports warnings.

        Raising on warnings implies retrieving warnings automatically. In
        other words: warnings will be set to True. If set to False, warnings
        will be also set to False.

        Raises ValueError on error.
        """
        if not isinstance(toggle, bool):
            raise ValueError("Expected a boolean type")
        self._raise_on_warnings = toggle
        self._get_warnings = toggle

    def _get_raise_on_warnings(self):
        """Get whether this connection raises an error on warnings

        This method returns whether this connection will raise errors when
        MySQL reports warnings.

        Returns True or False.
        """
        return self._raise_on_warnings

    raise_on_warnings = property(_get_raise_on_warnings,
                                 _set_raise_on_warnings,
                                 doc="Toggle wheter to raise on warnings "\
                                     "(emplies retrieving warnings).")

    def cursor(self, buffered=None, raw=None, cursor_class=None):
        """Instantiates and returns a cursor

        By default, MySQLCursor is returned. Depending on the options
        while connecting, a buffered and/or raw cursor instantiated
        instead.

        It is possible to also give a custom cursor through the
        cursor_class paramter, but it needs to be a subclass of
        mysql.connector.cursor.CursorBase.

        Returns a cursor-object
        """
        if not self.is_connected():
            raise errors.OperationalError("MySQL Connection not available.")
        if cursor_class is not None:
            if not issubclass(cursor_class, CursorBase):
                raise errors.ProgrammingError(
                    "Cursor class needs to be subclass of cursor.CursorBase")
            return (cursor_class)(self)

        buffered = buffered or self._buffered
        raw = raw or self._raw

        cursor_type = 0
        if buffered is True:
            cursor_type  |= 1
        if raw is True:
            cursor_type  |= 2

        types = (
            MySQLCursor, # 0
            MySQLCursorBuffered,
            MySQLCursorRaw,
            MySQLCursorBufferedRaw,
        )
        return (types[cursor_type ])(self)

    def commit(self):
        """Commit current transaction"""
        self._execute_query("COMMIT")

    def rollback(self):
        """Rollback current transaction"""
        self._execute_query("ROLLBACK")

    def _execute_query(self, query):
        """Execute a query

        This method simply calles cmd_query() after checking for unread
        result. If there are still unread result, an errors.InterfaceError
        is raised. Otherwise whatever cmd_query() returns is returned.

        Returns a dict()
        """
        if self._unread_result is True:
            raise errors.InternalError("Unread result found.")

        self.cmd_query(query)

    def _info_query(self, query):
        """Send a query which only returns 1 row"""
        cursor = self.cursor(buffered=True)
        cursor.execute(query)
        return cursor.fetchone()


