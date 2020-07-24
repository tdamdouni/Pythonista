# -*- coding: utf-8 -*-

# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2013, Oracle and/or its affiliates. All rights reserved.
# 
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

# This file was auto-generated.
_GENERATED_ON = '2013-01-28'
_MYSQL_VERSION = (5, 6, 9)

# Start MySQL Error messages
CR_UNKNOWN_ERROR = u"Unknown MySQL error"
CR_SOCKET_CREATE_ERROR = u"Can't create UNIX socket (%s)"
CR_CONNECTION_ERROR = u"Can't connect to local MySQL server through socket '%-.100s' (%s)"
CR_CONN_HOST_ERROR = u"Can't connect to MySQL server on '%-.100s' (%s)"
CR_IPSOCK_ERROR = u"Can't create TCP/IP socket (%s)"
CR_UNKNOWN_HOST = u"Unknown MySQL server host '%-.100s' (%s)"
CR_SERVER_GONE_ERROR = u"MySQL server has gone away"
CR_VERSION_ERROR = u"Protocol mismatch; server version = %s, client version = %s"
CR_OUT_OF_MEMORY = u"MySQL client ran out of memory"
CR_WRONG_HOST_INFO = u"Wrong host info"
CR_LOCALHOST_CONNECTION = u"Localhost via UNIX socket"
CR_TCP_CONNECTION = u"%-.100s via TCP/IP"
CR_SERVER_HANDSHAKE_ERR = u"Error in server handshake"
CR_SERVER_LOST = u"Lost connection to MySQL server during query"
CR_COMMANDS_OUT_OF_SYNC = u"Commands out of sync; you can't run this command now"
CR_NAMEDPIPE_CONNECTION = u"Named pipe: %-.32s"
CR_NAMEDPIPEWAIT_ERROR = u"Can't wait for named pipe to host: %-.64s  pipe: %-.32s (%s)"
CR_NAMEDPIPEOPEN_ERROR = u"Can't open named pipe to host: %-.64s  pipe: %-.32s (%s)"
CR_NAMEDPIPESETSTATE_ERROR = u"Can't set state of named pipe to host: %-.64s  pipe: %-.32s (%s)"
CR_CANT_READ_CHARSET = u"Can't initialize character set %-.32s (path: %-.100s)"
CR_NET_PACKET_TOO_LARGE = u"Got packet bigger than 'max_allowed_packet' bytes"
CR_EMBEDDED_CONNECTION = u"Embedded server"
CR_PROBE_SLAVE_STATUS = u"Error on SHOW SLAVE STATUS:"
CR_PROBE_SLAVE_HOSTS = u"Error on SHOW SLAVE HOSTS:"
CR_PROBE_SLAVE_CONNECT = u"Error connecting to subordinate:"
CR_PROBE_MASTER_CONNECT = u"Error connecting to main:"
CR_SSL_CONNECTION_ERROR = u"SSL connection error: %-.100s"
CR_MALFORMED_PACKET = u"Malformed packet"
CR_WRONG_LICENSE = u"This client library is licensed only for use with MySQL servers having '%s' license"
CR_NULL_POINTER = u"Invalid use of null pointer"
CR_NO_PREPARE_STMT = u"Statement not prepared"
CR_PARAMS_NOT_BOUND = u"No data supplied for parameters in prepared statement"
CR_DATA_TRUNCATED = u"Data truncated"
CR_NO_PARAMETERS_EXISTS = u"No parameters exist in the statement"
CR_INVALID_PARAMETER_NO = u"Invalid parameter number"
CR_INVALID_BUFFER_USE = u"Can't send long data for non-string/non-binary data types (parameter: %s)"
CR_UNSUPPORTED_PARAM_TYPE = u"Using unsupported buffer type: %s  (parameter: %s)"
CR_SHARED_MEMORY_CONNECTION = u"Shared memory: %-.100s"
CR_SHARED_MEMORY_CONNECT_REQUEST_ERROR = u"Can't open shared memory; client could not create request event (%s)"
CR_SHARED_MEMORY_CONNECT_ANSWER_ERROR = u"Can't open shared memory; no answer event received from server (%s)"
CR_SHARED_MEMORY_CONNECT_FILE_MAP_ERROR = u"Can't open shared memory; server could not allocate file mapping (%s)"
CR_SHARED_MEMORY_CONNECT_MAP_ERROR = u"Can't open shared memory; server could not get pointer to file mapping (%s)"
CR_SHARED_MEMORY_FILE_MAP_ERROR = u"Can't open shared memory; client could not allocate file mapping (%s)"
CR_SHARED_MEMORY_MAP_ERROR = u"Can't open shared memory; client could not get pointer to file mapping (%s)"
CR_SHARED_MEMORY_EVENT_ERROR = u"Can't open shared memory; client could not create %s event (%s)"
CR_SHARED_MEMORY_CONNECT_ABANDONED_ERROR = u"Can't open shared memory; no answer from server (%s)"
CR_SHARED_MEMORY_CONNECT_SET_ERROR = u"Can't open shared memory; cannot send request event to server (%s)"
CR_CONN_UNKNOW_PROTOCOL = u"Wrong or unknown protocol"
CR_INVALID_CONN_HANDLE = u"Invalid connection handle"
CR_SECURE_AUTH = u"Connection using old (pre-4.1.1) authentication protocol refused (client option 'secure_auth' enabled)"
CR_FETCH_CANCELED = u"Row retrieval was canceled by mysql_stmt_close() call"
CR_NO_DATA = u"Attempt to read column without prior row fetch"
CR_NO_STMT_METADATA = u"Prepared statement contains no metadata"
CR_NO_RESULT_SET = u"Attempt to read a row while there is no result set associated with the statement"
CR_NOT_IMPLEMENTED = u"This feature is not implemented yet"
CR_SERVER_LOST_EXTENDED = u"Lost connection to MySQL server at '%s', system error: %s"
CR_STMT_CLOSED = u"Statement closed indirectly because of a preceeding %s() call"
CR_NEW_STMT_METADATA = u"The number of columns in the result set differs from the number of bound buffers. You must reset the statement, rebind the result set columns, and execute the statement again"
CR_ALREADY_CONNECTED = u"This handle is already connected. Use a separate handle for each connection."
CR_AUTH_PLUGIN_CANNOT_LOAD = u"Authentication plugin '%s' cannot be loaded: %s"
CR_DUPLICATE_CONNECTION_ATTR = u""
# End MySQL Error messages

