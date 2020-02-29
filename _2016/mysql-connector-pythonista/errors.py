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

"""This module implements Exception classes
"""

import utils
import errorcode
from locales import get_client_error

_CUSTOM_ERROR_EXCEPTIONS = {}

def custom_error_exception(error=None, exception=None):
    """Define custom exceptions for MySQL server errors

    This function defines custom exceptions for MySQL server errors and
    returns the current set customizations.

    If error is a MySQL Server error number, then you have to pass also the
    exception class.

    The error argument can also be a dictionary in which case the key is
    the server error number, and value the exception to be raised.

    If none of the arguments are given, then custom_error_exception() will
    simply return the current set customizations.

    To reset the customizations, simply supply an empty dictionary.

    Examples:
        import mysql.connector
        from mysql.connector import errorcode

        # Server error 1028 should raise a DatabaseError
        mysql.connector.custom_error_exception(
            1028, mysql.connector.DatabaseError)

        # Or using a dictionary:
        mysql.connector.custom_error_exception({
            1028: mysql.connector.DatabaseError,
            1029: mysql.connector.OperationalError,
            })

        # Reset
        mysql.connector.custom_error_exception({})

    Returns a dictionary.
    """
    global _CUSTOM_ERROR_EXCEPTIONS

    if isinstance(error, dict) and not len(error):
        _CUSTOM_ERROR_EXCEPTIONS = {}
        return _CUSTOM_ERROR_EXCEPTIONS

    if not error and not exception:
        return _CUSTOM_ERROR_EXCEPTIONS

    if not isinstance(error, (int, dict)):
        raise ValueError(
            "The error argument should be either an integer or dictionary")

    if isinstance(error, int):
        error = { error: exception }

    for errno, exception in error.items():
        if not isinstance(errno, int):
            raise ValueError("error number should be an integer")
        try:
            if not issubclass(exception, Exception):
                raise TypeError
        except TypeError:
            raise ValueError("exception should be subclass of Exception")
        _CUSTOM_ERROR_EXCEPTIONS[errno] = exception

    return _CUSTOM_ERROR_EXCEPTIONS

def get_mysql_exception(errno, msg, sqlstate=None):
    """Get the exception matching the MySQL error
    
    This function will return an exception based on the SQLState. The given
    message will be passed on in the returned exception.

    The exception returned can be customized using the
    mysql.connector.custom_error_exception() function.
    
    Returns an Exception
    """
    try:
        return _CUSTOM_ERROR_EXCEPTIONS[errno](
            msg=msg, errno=errno, sqlstate=sqlstate)
    except KeyError:
        # Error was not mapped to particular exception
        pass

    if not sqlstate:
        return DatabaseError(msg=msg, errno=errno)

    try:
        return _SQLSTATE_CLASS_EXCEPTION[sqlstate[0:2]](
            msg=msg, errno=errno, sqlstate=sqlstate)
    except KeyError:
        # Return default InterfaceError
        return DatabaseError(msg=msg, errno=errno, sqlstate=sqlstate)

def get_exception(packet):
    """Returns an exception object based on the MySQL error
    
    Returns an exception object based on the MySQL error in the given
    packet.
    
    Returns an Error-Object.
    """
    errno = errmsg = None
    
    if packet[4] != '\xff':
        raise ValueError("Packet is not an error packet")
    
    sqlstate = None
    try:
        packet = packet[5:]
        (packet, errno) = utils.read_int(packet, 2)
        if packet[0] != '\x23':
            # Error without SQLState
            errmsg = packet
        else:
            (packet, sqlstate) = utils.read_bytes(packet[1:], 5)
            errmsg = packet
    except Exception as err:
        return InterfaceError("Failed getting Error information (%r)" % err)
    else:
        return get_mysql_exception(errno, errmsg, sqlstate)

class Error(StandardError):
    """Exception that is base class for all other error exceptions"""
    def __init__(self, msg=None, errno=None, values=None, sqlstate=None):
        self.msg = msg
        self.errno = errno or -1
        self.sqlstate = sqlstate
        
        if not self.msg and (2000 <= self.errno < 3000):
            errmsg = get_client_error(self.errno)
            if values is not None:
                try:
                    errmsg = errmsg % values
                except TypeError as err:
                    errmsg = errmsg + " (Warning: %s)" % err
            self.msg = errmsg
        elif not self.msg:
            self.msg = 'Unknown error'
        
        if self.msg and self.errno != -1:
            if self.sqlstate:
                self.msg = '%d (%s): %s' % (self.errno, self.sqlstate,
                                            self.msg)
            else:
                self.msg = '%d: %s' % (self.errno, self.msg)
    
    def __str__(self):
        return self.msg
        
class Warning(StandardError):
    """Exception for important warnings"""
    pass

class InterfaceError(Error):
    """Exception for errors related to the interface"""
    pass

class DatabaseError(Error):
    """Exception for errors related to the database"""
    pass

class InternalError(DatabaseError):
    """Exception for errors internal database errors"""
    pass

class OperationalError(DatabaseError):
    """Exception for errors related to the database's operation"""
    pass

class ProgrammingError(DatabaseError):
    """Exception for errors programming errors"""
    pass

class IntegrityError(DatabaseError):
    """Exception for errors regarding relational integrity"""
    pass

class DataError(DatabaseError):
    """Exception for errors reporting problems with processed data"""
    pass

class NotSupportedError(DatabaseError):
    """Exception for errors when an unsupported database feature was used"""
    pass

_SQLSTATE_CLASS_EXCEPTION = {
    '02': DataError, # no data
    '07': DatabaseError, # dynamic SQL error
    '08': OperationalError, # connection exception
    '0A': NotSupportedError, # feature not supported
    '21': DataError, # cardinality violation
    '22': DataError, # data exception
    '23': IntegrityError, # integrity constraint violation
    '24': ProgrammingError, # invalid cursor state
    '25': ProgrammingError, # invalid transaction state
    '26': ProgrammingError, # invalid SQL statement name
    '27': ProgrammingError, # triggered data change violation
    '28': ProgrammingError, # invalid authorization specification
    '2A': ProgrammingError, # direct SQL syntax error or access rule violation
    '2B': DatabaseError, # dependent privilege descriptors still exist
    '2C': ProgrammingError, # invalid character set name
    '2D': DatabaseError, # invalid transaction termination
    '2E': DatabaseError, # invalid connection name
    '33': DatabaseError, # invalid SQL descriptor name
    '34': ProgrammingError, # invalid cursor name
    '35': ProgrammingError, # invalid condition number
    '37': ProgrammingError, # dynamic SQL syntax error or access rule violation
    '3C': ProgrammingError, # ambiguous cursor name
    '3D': ProgrammingError, # invalid catalog name
    '3F': ProgrammingError, # invalid schema name
    '40': InternalError, # transaction rollback
    '42': ProgrammingError, # syntax error or access rule violation
    '44': InternalError, # with check option violation
    'HZ': OperationalError, # remote database access
    'XA': IntegrityError,
    '0K': OperationalError,
    'HY': DatabaseError, # default when no SQLState provided by MySQL server
}

