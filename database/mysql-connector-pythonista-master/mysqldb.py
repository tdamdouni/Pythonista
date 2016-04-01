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

"""
MySQL Connector/Python - MySQL drive written in Python
"""

# Python Db API v2
apilevel = '2.0'
threadsafety = 1
paramstyle = 'pyformat'

from connection import MySQLConnection
from errors import (
    Error, Warning, InterfaceError, DatabaseError, 
    NotSupportedError, DataError, IntegrityError, ProgrammingError, 
    OperationalError, InternalError, custom_error_exception)
from constants import (FieldFlag, FieldType, CharacterSet,
    RefreshOption, ClientFlag)
from dbapi import *

def Connect(*args, **kwargs):
    """Shortcut for creating a connection.MySQLConnection object."""
    return MySQLConnection(*args, **kwargs)
connect = Connect

__all__ = [
    'MySQLConnection', 'Connect', 'custom_error_exception',
    
    # Some useful constants
    'FieldType','FieldFlag','ClientFlag','CharacterSet','RefreshOption',

    # Error handling
    'Error','Warning',
    'InterfaceError','DatabaseError',
    'NotSupportedError','DataError','IntegrityError','ProgrammingError',
    'OperationalError','InternalError',
    
    # DBAPI PEP 249 required exports
    'connect','apilevel','threadsafety','paramstyle',
    'Date', 'Time', 'Timestamp', 'Binary',
    'DateFromTicks', 'DateFromTicks', 'TimestampFromTicks',
    'STRING', 'BINARY', 'NUMBER',
    'DATETIME', 'ROWID',
    ]
