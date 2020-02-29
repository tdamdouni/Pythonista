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

"""Cursor classes
"""

import sys
import weakref
import re
import itertools

import errors

RE_SQL_COMMENT = re.compile("\/\*.*\*\/")
RE_SQL_INSERT_VALUES = re.compile(
    r'VALUES\s*(\(\s*(?:%(?:\(.*\)|)s\s*(?:,|)\s*)+\))',
    re.I | re.M)
RE_SQL_INSERT_STMT = re.compile(r'INSERT\s+INTO', re.I)
RE_SQL_SPLIT_STMTS = re.compile(
    r''';(?=(?:[^"'`]*["'`][^"'`]*["'`])*[^"'`]*$)''')

class CursorBase(object):
    """
    Base for defining MySQLCursor. This class is a skeleton and defines
    methods and members as required for the Python Database API
    Specification v2.0.
    
    It's better to inherite from MySQLCursor.
    """
    
    def __init__(self):
        self._description = None
        self._rowcount = -1
        self._last_insert_id = None
        self.arraysize = 1
    
    def callproc(self, procname, args=()):
        pass
    
    def close(self):
        pass
    
    def execute(self, operation, params=()):
        pass
    
    def executemany(self, operation, seqparams):
        pass
    
    def fetchone(self):
        pass
    
    def fetchmany(self, size=1):
        pass
    
    def fetchall(self):
        pass
    
    def nextset(self):
        pass
    
    def setinputsizes(self, sizes):
        pass
    
    def setoutputsize(self, size, column=None):
        pass
    
    def reset(self):
        pass

    @property
    def description(self):
        """Returns description of columns in a result

        This property returns a list of tuples describing the columns in
        in a result set. A tuple is described as follows::

                (column_name,
                 type,
                 None,
                 None,
                 None,
                 None,
                 null_ok,
                 column_flags)  # Addition to PEP-249 specs

        Returns a list of tuples.
        """
        return self._description

    @property
    def rowcount(self):
        """Returns the number of rows produced or affected
        
        This property returns the number of rows produced by queries
        such as a SELECT, or affected rows when executing DML statements
        like INSERT or UPDATE.
        
        Note that for non-buffered cursors it is impossible to know the
        number of rows produced before having fetched them all. For those,
        the number of rows will be -1 right after execution, and
        incremented when fetching rows.
        
        Returns an integer.
        """
        return self._rowcount

    @property
    def lastrowid(self):
        """Returns the value generated for an AUTO_INCREMENT column
        
        Returns the value generated for an AUTO_INCREMENT column by
        the previous INSERT or UPDATE statement or None when there is
        no such value available.
        
        Returns a long value or None.
        """
        return self._last_insert_id

class MySQLCursor(CursorBase):
    """Default cursor for interacting with MySQL
    
    This cursor will execute statements and handle the result. It will
    not automatically fetch all rows.
    
    MySQLCursor should be inherited whenever other functionallity is
    required. An example would to change the fetch* member functions
    to return dictionaries instead of lists of values.
    
    Implements the Python Database API Specification v2.0 (PEP-249)
    """
    def __init__(self, connection=None):
        CursorBase.__init__(self)
        self._connection = None
        self._stored_results = []
        self._nextrow = (None, None)
        self._warnings = None
        self._warning_count = 0
        self._executed = None
        self._executed_list = []
        
        if connection is not None:
            self._set_connection(connection)
    
    def __iter__(self):
        """
        Iteration over the result set which calls self.fetchone()
        and returns the next row.
        """
        return iter(self.fetchone, None)
        
    def _set_connection(self, connection):
        try:
            self._connection = weakref.proxy(connection)
            self._connection._protocol
        except (AttributeError, TypeError):
            raise errors.InterfaceError(errno=2048)

    def _reset_result(self):
        self._rowcount = -1
        self._lastrowid = None
        self._nextrow = (None, None)
        self._stored_results = []
        self._warnings = None
        self._warning_count = 0
        self._description = None
        self._executed = None
        self._executed_list = []
        self.reset()

    def _have_unread_result(self):
        """Check whether there is an unread result"""
        try:
            return self._connection.unread_result
        except AttributeError:
            return False
        
    def next(self):
        """
        Used for iterating over the result set. Calles self.fetchone()
        to get the next row.
        """
        try:
            row = self.fetchone()
        except errors.InterfaceError:
            raise StopIteration
        if not row:
            raise StopIteration
        return row
    
    def close(self):
        """Close the cursor
        
        Returns True when successful, otherwise False.
        """
        if self._connection is None:
            return False
        
        self._reset_result()
        self._connection = None
        
        return True

    def _process_params_dict(self, params):
        try:
            to_mysql = self._connection.converter.to_mysql
            escape = self._connection.converter.escape
            quote = self._connection.converter.quote
            res = {}
            for k,v in params.items():
                c = v
                c = to_mysql(c)
                c = escape(c)
                c = quote(c)
                res[k] = c
        except StandardError as e:
            raise errors.ProgrammingError(
                "Failed processing pyformat-parameters; %s" % e)
        else:
            return res
            
        return None
    
    def _process_params(self, params):
        """
        Process the parameters which were given when self.execute() was
        called. It does following using the MySQLConnection converter:
        * Convert Python types to MySQL types
        * Escapes characters required for MySQL.
        * Quote values when needed.
        
        Returns a list.
        """
        if isinstance(params,dict):
            return self._process_params_dict(params)
        
        try:
            res = params
            res = map(self._connection.converter.to_mysql,res)
            res = map(self._connection.converter.escape,res)
            res = map(self._connection.converter.quote,res)
        except StandardError as e:
            raise errors.ProgrammingError(
                "Failed processing format-parameters; %s" % e)
        else:
            return tuple(res)
        return None

    def _row_to_python(self, rowdata, desc=None):
        res = ()
        try:
            if not desc:
                desc = self.description
            for idx,v in enumerate(rowdata):
                flddsc = desc[idx]
                res += (self._connection.converter.to_python(flddsc, v),)
        except StandardError as e:
            raise errors.InterfaceError(
                "Failed converting row to Python types; %s" % e)
        else:
            return res
    
        return None
        
    def _handle_noresultset(self, res):
        """Handles result of execute() when there is no result set
        """
        try:
            self._rowcount = res['affected_rows']
            self._last_insert_id = res['insert_id']
            self._warning_count = res['warning_count']
        except (KeyError, TypeError) as err:
            raise errors.ProgrammingError(
                "Failed handling non-resultset; %s" % err)
        
        if self._connection.get_warnings is True and self._warning_count:
                self._warnings = self._fetch_warnings()
        
    def _handle_resultset(self):
        pass
    
    def _handle_result(self, result):
        """
        Handle the result after a command was send. The result can be either
        an OK-packet or a dictionary containing column/eof information.
        
        Raises InterfaceError when result is not a dict() or result is
        invalid.
        """
        if not isinstance(result, dict):
            raise errors.InterfaceError('Result was not a dict()')
        
        if 'columns' in result:
            # Weak test, must be column/eof information
            self._description = result['columns']
            self._connection.unread_result = True
            self._handle_resultset()
        elif 'affected_rows' in result:
            # Weak test, must be an OK-packet
            self._connection.unread_result = False
            self._handle_noresultset(result)
        else:
            raise errors.InterfaceError('Invalid result')
    
    def _execute_iter(self, query_iter):
        """Generator returns MySQLCursor objects for multiple statements
        
        This method is only used when multiple statements are executed
        by the execute() method. It uses itertools.izip to iterate over the
        given query_iter (result of MySQLConnection.cmd_query_iter()) and
        the list of statements that were executed.
        
        Yields a MySQLCursor instance.
        """
        if not self._executed_list:
            self._executed_list = RE_SQL_SPLIT_STMTS.split(self._executed)
        
        for result, stmt in itertools.izip(query_iter,
                                           iter(self._executed_list)):
            self._reset_result()
            self._handle_result(result)
            self._executed = stmt
            yield self
    
    def execute(self, operation, params=None, multi=False):
        """Executes the given operation
        
        Executes the given operation substituting any markers with
        the given parameters.
        
        For example, getting all rows where id is 5:
          cursor.execute("SELECT * FROM t1 WHERE id = %s", (5,))
        
        The multi argument should be set to True when executing multiple
        statements in one operation. If not set and multiple results are
        found, an InterfaceError will be raised.
        
        If warnings where generated, and connection.get_warnings is True, then
        self._warnings will be a list containing these warnings.
        
        Returns an iterator when multi is True, otherwise None.
        """
        if not operation:
            return
        if self._have_unread_result():
            raise errors.InternalError("Unread result found.")
        
        self._reset_result()
        stmt = ''
        
        try:
            if isinstance(operation, unicode):
                operation = operation.encode(self._connection.charset)
        except (UnicodeDecodeError, UnicodeEncodeError) as e:
            raise errors.ProgrammingError(str(e))
            
        if params is not None:
            try:
                stmt = operation % self._process_params(params)
            except TypeError:
                raise errors.ProgrammingError(
                    "Wrong number of arguments during string formatting")
        else:
            stmt = operation
        
        if multi:
            self._executed = stmt
            self._executed_list = []
            return self._execute_iter(self._connection.cmd_query_iter(stmt))
        else:
            self._executed = stmt
            try:
                self._handle_result(self._connection.cmd_query(stmt))
            except errors.InterfaceError as err:
                if self._connection._have_next_result:
                    raise errors.InterfaceError(
                        "Use multi=True when executing multiple statements")
                raise
            return None

    def executemany(self, operation, seq_params):
        """Execute the given operation multiple times
        
        The executemany() method will execute the operation iterating
        over the list of parameters in seq_params.
        
        Example: Inserting 3 new employees and their phone number
        
        data = [
            ('Jane','555-001'),
            ('Joe', '555-001'),
            ('John', '555-003')
            ]
        stmt = "INSERT INTO employees (name, phone) VALUES ('%s','%s')"
        cursor.executemany(stmt, data)
        
        INSERT statements are optimized by batching the data, that is
        using the MySQL multiple rows syntax.
        
        Results are discarded. If they are needed, consider looping over
        data using the execute() method.
        """
        if not operation:
            return
        if self._have_unread_result():
            raise errors.InternalError("Unread result found.")
        elif len(RE_SQL_SPLIT_STMTS.split(operation)) > 1:
            raise errors.InternalError(
                "executemany() does not support multiple statements")
        
        # Optimize INSERTs by batching them
        if re.match(RE_SQL_INSERT_STMT,operation):
            opnocom = re.sub(RE_SQL_COMMENT, '', operation)
            m = re.search(RE_SQL_INSERT_VALUES, opnocom)
            fmt = m.group(1)
            values = []
            for params in seq_params:
                values.append(fmt % self._process_params(params))
            operation = operation.replace(m.group(1), ','.join(values), 1)
            return self.execute(operation)
            
        rowcnt = 0
        try:
            for params in seq_params:
                self.execute(operation, params)
                if self.with_rows and self._have_unread_result():
                    self.fetchall()
                rowcnt += self._rowcount
        except (ValueError, TypeError) as err:
            raise errors.InterfaceError(
                "Failed executing the operation; %s" % err)
        except:
            # Raise whatever execute() raises
            raise
        self._rowcount = rowcnt

    def stored_results(self):
        """Returns an iterator for stored results
        
        This method returns an iterator over results which are stored when
        callproc() is called. The iterator will provide MySQLCursorBuffered
        instances.
        
        Returns a iterator.
        """
        return iter(self._stored_results)

    def callproc(self, procname, args=()):
        """Calls a stored procedue with the given arguments

        The arguments will be set during this session, meaning
        they will be called like  _<procname>__arg<nr> where
        <nr> is an enumeration (+1) of the arguments.

        Coding Example:
          1) Definining the Stored Routine in MySQL:
          CREATE PROCEDURE multiply(IN pFac1 INT, IN pFac2 INT, OUT pProd INT)
          BEGIN
            SET pProd := pFac1 * pFac2;
          END

          2) Executing in Python:
          args = (5,5,0) # 0 is to hold pprod
          cursor.callproc('multiply', args)
          print cursor.fetchone()

        Does not return a value, but a result set will be
        available when the CALL-statement execute successfully.
        Raises exceptions when something is wrong.
        """
        if not procname or not isinstance(procname, str):
            raise ValueError("procname must be a string")

        if not isinstance(args, (tuple, list)):
            raise ValueError("args must be a sequence")

        argfmt = "@_%s_arg%d"
        self._stored_results = []

        results = []
        try:
            argnames = []

            if args:
                for idx,arg in enumerate(args):
                    argname = argfmt % (procname, idx+1)
                    argnames.append(argname)
                    self.execute("SET %s=%%s" % (argname), (arg,))

            call = "CALL %s(%s)" % (procname,','.join(argnames))
            
            for result in self._connection.cmd_query_iter(call):
                if 'columns' in result:
                    tmp = MySQLCursorBuffered(self._connection._get_self())
                    tmp._handle_result(result)
                    results.append(tmp)

            if argnames:
                select = "SELECT %s" % ','.join(argnames)
                self.execute(select)
                self._stored_results = results
                return self.fetchone()
            else:
                self._stored_results = results
                return ()

        except errors.Error:
            raise
        except StandardError as e:
            raise errors.InterfaceError(
                "Failed calling stored routine; %s" % e)

    def getlastrowid(self):
        """Returns the value generated for an AUTO_INCREMENT column
        
        This method is kept for backward compatibility. Please use the
        property lastrowid instead.
        
        Returns a long value or None.
        """
        return self.lastrowid
        
    def _fetch_warnings(self):
        """
        Fetch warnings doing a SHOW WARNINGS. Can be called after getting
        the result.

        Returns a result set or None when there were no warnings.
        """
        res = []
        try:
            c = self._connection.cursor()
            cnt = c.execute("SHOW WARNINGS")
            res = c.fetchall()
            c.close()
        except StandardError as e:
            raise errors.InterfaceError, errors.InterfaceError(
                "Failed getting warnings; %s" % e), sys.exc_info()[2]
        
        if self._connection.raise_on_warnings is True:
            msg = '; '.join([ "(%s) %s" % (r[1],r[2]) for r in res])
            raise errors.get_mysql_exception(res[0][1],res[0][2])
        else:
            if len(res):
                return res
            
        return None
    
    def _handle_eof(self, eof):
        self._connection.unread_result = False
        self._nextrow = (None, None)
        self._warning_count = eof['warning_count']
        if self._connection.get_warnings is True and eof['warning_count']:
            self._warnings = self._fetch_warnings()
        
    def _fetch_row(self):
        if not self._have_unread_result():
            return None
        row = None
        try:
            if self._nextrow == (None, None):
                (row, eof) = self._connection.get_row()
            else:
                (row, eof) = self._nextrow
            if row:
                (foo, eof) = self._nextrow = self._connection.get_row()
                if eof is not None:
                    self._handle_eof(eof)
                if self._rowcount == -1:
                    self._rowcount = 1
                else:
                    self._rowcount += 1
            if eof:
                self._handle_eof(eof)
        except:
            raise
        else:
            return row
            
        return None
    
    def fetchwarnings(self):
        return self._warnings
        
    def fetchone(self):
        row = self._fetch_row()
        if row:
            return self._row_to_python(row)
        return None
        
    def fetchmany(self,size=None):
        res = []
        cnt = (size or self.arraysize)
        while cnt > 0 and self._have_unread_result():
            cnt -= 1
            row = self.fetchone()
            if row:
                res.append(row)
            
        return res
    
    def fetchall(self):
        if not self._have_unread_result():
            raise errors.InterfaceError("No result set to fetch from.")
        res = []
        (rows, eof) = self._connection.get_rows()
        self._rowcount = len(rows)
        for i in xrange(0,self.rowcount):
            res.append(self._row_to_python(rows[i]))
        self._handle_eof(eof)
        return res
    
    @property
    def column_names(self):
        """Returns column names
        
        This property returns the columns names as a tuple.
        
        Returns a tuple.
        """
        if not self.description:
            return ()
        return tuple( [d[0].decode('utf8') for d in self.description] )
    
    @property
    def statement(self):
        """Returns the executed statement
        
        This property returns the executed statement. When multiple
        statements were executed, the current statement in the iterator
        will be returned.
        """
        return self._executed.strip()
    
    @property
    def with_rows(self):
        """Returns whether the cursor could have rows returned
        
        This property returns True when column descriptions are available
        and possibly also rows, which will need to be fetched.
        
        Returns True or False.
        """
        if not self.description:
            return False
        return True
        
    def __unicode__(self):
        fmt = "MySQLCursor: %s"
        if self._executed:
            if len(self._executed) > 30:
                res = fmt % (self._executed[:30] + '..')
            else:
                res = fmt % (self._executed)
        else:
            res = fmt % '(Nothing executed yet)'
        return res
    
    def __str__(self):
        return repr(self.__unicode__())

class MySQLCursorBuffered(MySQLCursor):
    """Cursor which fetches rows within execute()"""
    
    def __init__(self, connection=None):
        MySQLCursor.__init__(self, connection)
        self._rows = None
        self._next_row = 0
    
    def _handle_resultset(self):
        (self._rows, eof) = self._connection.get_rows()
        self._rowcount = len(self._rows)
        self._handle_eof(eof)
        self._next_row = 0
        try:
            self._connection.unread_result = False
        except:
            pass
        
    def reset(self):
        self._rows = None

    def _fetch_row(self):
        row = None
        try:
            row = self._rows[self._next_row]
        except:
            return None
        else:
            self._next_row += 1
            return row
        return None
    
    def fetchall(self):
        if self._rows is None:
            raise errors.InterfaceError("No result set to fetch from.")
        res = []
        for row in self._rows:
            res.append(self._row_to_python(row))
        self._next_row = len(self._rows)
        return res
    
    def fetchmany(self,size=None):
        res = []
        cnt = (size or self.arraysize)
        while cnt > 0:
            cnt -= 1
            row = self.fetchone()
            if row:
                res.append(row)

        return res

    @property
    def with_rows(self):
        return self._rows is not None

class MySQLCursorRaw(MySQLCursor):

    def fetchone(self):
        row = self._fetch_row()
        if row:
            return row
        return None
    
    def fetchall(self):
        if not self._have_unread_result():
            raise errors.InterfaceError("No result set to fetch from.")
        (rows, eof) = self._connection.get_rows()
        self._rowcount = len(rows)
        self._handle_eof(eof)
        return rows
        
class MySQLCursorBufferedRaw(MySQLCursorBuffered):
    
    def fetchone(self):
        row = self._fetch_row()
        if row:
            return row
        return None
    
    def fetchall(self):
        if self._rows is None:
            raise errors.InterfaceError("No result set to fetch from.")
        return [ r for r in self._rows ]

