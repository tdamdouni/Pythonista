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

"""Various MySQL constants and character sets
"""

from errors import ProgrammingError

MAX_PACKET_LENGTH = 16777215
RESULT_WITHOUT_ROWS = 0
RESULT_WITH_ROWS = 1

def flag_is_set(flag, flags):
    """Checks if the flag is set
    
    Returns boolean"""
    if (flags & flag) > 0:
        return True
    return False

class _constants(object):
    
    prefix = ''
    desc = {}
    
    def __new__(cls):
        raise TypeError, "Can not instanciate from %s" % cls.__name__
        
    @classmethod
    def get_desc(cls,name):
        try:
            return cls.desc[name][1]
        except:
            return None
            
    @classmethod
    def get_info(cls,n):
        for name, info in cls.desc.items():
            if info[0] == n:
                return name
        return None
    
    @classmethod
    def get_full_info(cls):
        res = ()
        try:
            res = ["%s : %s" % (k,v[1]) for k,v in cls.desc.items()]
        except StandardError as e:
            res = ('No information found in constant class.%s' % e)
        
        return res

class _constantflags(_constants):
    
    @classmethod
    def get_bit_info(cls, v):
        """Get the name of all bits set
        
        Returns a list of strings."""
        res = []
        for name,d in cls.desc.items():
            if v & d[0]:
                res.append(name)
        return res
    
class FieldType(_constants):
    
    prefix = 'FIELD_TYPE_'
    DECIMAL     = 0x00
    TINY        = 0x01
    SHORT       = 0x02
    LONG        = 0x03
    FLOAT       = 0x04
    DOUBLE      = 0x05
    NULL        = 0x06
    TIMESTAMP   = 0x07
    LONGLONG    = 0x08
    INT24       = 0x09
    DATE        = 0x0a
    TIME        = 0x0b
    DATETIME    = 0x0c
    YEAR        = 0x0d
    NEWDATE     = 0x0e
    VARCHAR     = 0x0f
    BIT         = 0x10
    NEWDECIMAL  = 0xf6
    ENUM        = 0xf7
    SET         = 0xf8
    TINY_BLOB   = 0xf9
    MEDIUM_BLOB = 0xfa
    LONG_BLOB   = 0xfb
    BLOB        = 0xfc
    VAR_STRING  = 0xfd
    STRING      = 0xfe
    GEOMETRY    = 0xff
    
    desc = {
        'DECIMAL':       (0x00, 'DECIMAL'),
        'TINY':          (0x01, 'TINY'),
        'SHORT':         (0x02, 'SHORT'),
        'LONG':          (0x03, 'LONG'),
        'FLOAT':         (0x04, 'FLOAT'),
        'DOUBLE':        (0x05, 'DOUBLE'),
        'NULL':          (0x06, 'NULL'),
        'TIMESTAMP':     (0x07, 'TIMESTAMP'),
        'LONGLONG':      (0x08, 'LONGLONG'),
        'INT24':         (0x09, 'INT24'),
        'DATE':          (0x0a, 'DATE'),
        'TIME':          (0x0b, 'TIME'),
        'DATETIME':      (0x0c, 'DATETIME'),
        'YEAR':          (0x0d, 'YEAR'),
        'NEWDATE':       (0x0e, 'NEWDATE'),
        'VARCHAR':       (0x0f, 'VARCHAR'),
        'BIT':           (0x10, 'BIT'),
        'NEWDECIMAL':    (0xf6, 'NEWDECIMAL'),
        'ENUM':          (0xf7, 'ENUM'),
        'SET':           (0xf8, 'SET'),
        'TINY_BLOB':     (0xf9, 'TINY_BLOB'),
        'MEDIUM_BLOB':   (0xfa, 'MEDIUM_BLOB'),
        'LONG_BLOB':     (0xfb, 'LONG_BLOB'),
        'BLOB':          (0xfc, 'BLOB'),
        'VAR_STRING':    (0xfd, 'VAR_STRING'),
        'STRING':        (0xfe, 'STRING'),
        'GEOMETRY':      (0xff, 'GEOMETRY'),
    }
    
    @classmethod
    def get_string_types(cls):
        return [
            cls.VARCHAR,
            cls.ENUM,
            cls.VAR_STRING, cls.STRING,
            ]
    
    @classmethod
    def get_binary_types(cls):
        return [
            cls.TINY_BLOB, cls.MEDIUM_BLOB,
            cls.LONG_BLOB, cls.BLOB,
            ]
    
    @classmethod
    def get_number_types(cls):
        return [
            cls.DECIMAL, cls.NEWDECIMAL,
            cls.TINY, cls.SHORT, cls.LONG,
            cls.FLOAT, cls.DOUBLE,
            cls.LONGLONG, cls.INT24,
            cls.BIT,
            cls.YEAR,
            ]
    
    @classmethod
    def get_timestamp_types(cls):
        return [
            cls.DATETIME, cls.TIMESTAMP,
            ]

class FieldFlag(_constantflags):
    """
    Field flags as found in MySQL sources mysql-src/include/mysql_com.h
    """
    _prefix = ''
    NOT_NULL             = 1 <<  0
    PRI_KEY              = 1 <<  1
    UNIQUE_KEY           = 1 <<  2
    MULTIPLE_KEY         = 1 <<  3
    BLOB                 = 1 <<  4
    UNSIGNED             = 1 <<  5
    ZEROFILL             = 1 <<  6
    BINARY               = 1 <<  7

    ENUM                 = 1 <<  8
    AUTO_INCREMENT       = 1 <<  9
    TIMESTAMP            = 1 << 10
    SET                  = 1 << 11

    NO_DEFAULT_VALUE     = 1 << 12
    ON_UPDATE_NOW        = 1 << 13
    NUM                  = 1 << 14
    PART_KEY             = 1 << 15
    GROUP                = 1 << 14    # SAME AS NUM !!!!!!!????
    UNIQUE               = 1 << 16
    BINCMP               = 1 << 17

    GET_FIXED_FIELDS     = 1 << 18
    FIELD_IN_PART_FUNC   = 1 << 19
    FIELD_IN_ADD_INDEX   = 1 << 20
    FIELD_IS_RENAMED     = 1 << 21

    desc = {
        'NOT_NULL':             (1 <<  0, "Field can't be NULL"),
        'PRI_KEY':              (1 <<  1, "Field is part of a primary key"),
        'UNIQUE_KEY':           (1 <<  2, "Field is part of a unique key"),
        'MULTIPLE_KEY':         (1 <<  3, "Field is part of a key"),
        'BLOB':                 (1 <<  4, "Field is a blob"),
        'UNSIGNED':             (1 <<  5, "Field is unsigned"),
        'ZEROFILL':             (1 <<  6, "Field is zerofill"),
        'BINARY':               (1 <<  7, "Field is binary  "),
        'ENUM':                 (1 <<  8, "field is an enum"),
        'AUTO_INCREMENT':       (1 <<  9, "field is a autoincrement field"),
        'TIMESTAMP':            (1 << 10, "Field is a timestamp"),
        'SET':                  (1 << 11, "field is a set"),
        'NO_DEFAULT_VALUE':     (1 << 12, "Field doesn't have default value"),
        'ON_UPDATE_NOW':        (1 << 13, "Field is set to NOW on UPDATE"),
        'NUM':                  (1 << 14, "Field is num (for clients)"),

        'PART_KEY':             (1 << 15, "Intern; Part of some key"),
        'GROUP':                (1 << 14, "Intern: Group field"),   # Same as NUM
        'UNIQUE':               (1 << 16, "Intern: Used by sql_yacc"),
        'BINCMP':               (1 << 17, "Intern: Used by sql_yacc"),
        'GET_FIXED_FIELDS':     (1 << 18, "Used to get fields in item tree"),
        'FIELD_IN_PART_FUNC':   (1 << 19, "Field part of partition func"),
        'FIELD_IN_ADD_INDEX':        (1 << 20, "Intern: Field used in ADD INDEX"),
        'FIELD_IS_RENAMED':          (1 << 21, "Intern: Field is being renamed"),
    }
        
class ServerCmd(_constants):
    _prefix = 'COM_'
    SLEEP           =  0
    QUIT            =  1
    INIT_DB         =  2 
    QUERY           =  3
    FIELD_LIST      =  4
    CREATE_DB       =  5
    DROP_DB         =  6
    REFRESH         =  7
    SHUTDOWN        =  8
    STATISTICS      =  9
    PROCESS_INFO    = 10
    CONNECT         = 11
    PROCESS_KILL    = 12
    DEBUG           = 13
    PING            = 14
    TIME            = 15
    DELAYED_INSERT  = 16
    CHANGE_USER     = 17
    BINLOG_DUMP     = 18
    TABLE_DUMP      = 19
    CONNECT_OUT     = 20
    REGISTER_SLAVE  = 21
    STMT_PREPARE    = 22
    STMT_EXECUTE    = 23
    STMT_SEND_LONG_DATA = 24
    STMT_CLOSE      = 25
    STMT_RESET      = 26
    SET_OPTION      = 27
    STMT_FETCH      = 28
    DAEMON          = 29
    
    desc = {
        'SLEEP': (0,'SLEEP'),
        'QUIT': (1,'QUIT'),
        'INIT_DB': (2,'INIT_DB'), 
        'QUERY': (3,'QUERY'),
        'FIELD_LIST': (4,'FIELD_LIST'),
        'CREATE_DB': (5,'CREATE_DB'),
        'DROP_DB': (6,'DROP_DB'),
        'REFRESH': (7,'REFRESH'),
        'SHUTDOWN': (8,'SHUTDOWN'),
        'STATISTICS': (9,'STATISTICS'),
        'PROCESS_INFO': (10,'PROCESS_INFO'),
        'CONNECT': (11,'CONNECT'),
        'PROCESS_KILL': (12,'PROCESS_KILL'),
        'DEBUG': (13,'DEBUG'),
        'PING': (14,'PING'),
        'TIME': (15,'TIME'),
        'DELAYED_INSERT': (16,'DELAYED_INSERT'),
        'CHANGE_USER': (17,'CHANGE_USER'),
        'BINLOG_DUMP': (18,'BINLOG_DUMP'),
        'TABLE_DUMP': (19,'TABLE_DUMP'),
        'CONNECT_OUT': (20,'CONNECT_OUT'),
        'REGISTER_SLAVE': (21,'REGISTER_SLAVE'),
        'STMT_PREPARE': (22,'STMT_PREPARE'),
        'STMT_EXECUTE': (23,'STMT_EXECUTE'),
        'STMT_SEND_LONG_DATA': (24,'STMT_SEND_LONG_DATA'),
        'STMT_CLOSE': (25,'STMT_CLOSE'),
        'STMT_RESET': (26,'STMT_RESET'),
        'SET_OPTION': (27,'SET_OPTION'),
        'STMT_FETCH': (28,'STMT_FETCH'),
        'DAEMON': (29,'DAEMON'),
    }

class ClientFlag(_constantflags):
    """
    Client Options as found in the MySQL sources mysql-src/include/mysql_com.h
    """
    LONG_PASSWD             = 1 << 0
    FOUND_ROWS              = 1 << 1
    LONG_FLAG               = 1 << 2
    CONNECT_WITH_DB         = 1 << 3
    NO_SCHEMA               = 1 << 4
    COMPRESS                = 1 << 5
    ODBC                    = 1 << 6
    LOCAL_FILES             = 1 << 7
    IGNORE_SPACE            = 1 << 8
    PROTOCOL_41             = 1 << 9
    INTERACTIVE             = 1 << 10
    SSL                     = 1 << 11
    IGNORE_SIGPIPE          = 1 << 12
    TRANSACTIONS            = 1 << 13
    RESERVED                = 1 << 14
    SECURE_CONNECTION       = 1 << 15
    MULTI_STATEMENTS        = 1 << 16
    MULTI_RESULTS           = 1 << 17
    SSL_VERIFY_SERVER_CERT  = 1 << 30
    REMEMBER_OPTIONS        = 1 << 31
    
    desc = {
        'LONG_PASSWD':        (1 <<  0, 'New more secure passwords'),
        'FOUND_ROWS':         (1 <<  1, 'Found instead of affected rows'),
        'LONG_FLAG':          (1 <<  2, 'Get all column flags'),
        'CONNECT_WITH_DB':    (1 <<  3, 'One can specify db on connect'),
        'NO_SCHEMA':          (1 <<  4, "Don't allow database.table.column"),
        'COMPRESS':           (1 <<  5, 'Can use compression protocol'),
        'ODBC':               (1 <<  6, 'ODBC client'),
        'LOCAL_FILES':        (1 <<  7, 'Can use LOAD DATA LOCAL'),
        'IGNORE_SPACE':       (1 <<  8, "Ignore spaces before ''"),
        'PROTOCOL_41':        (1 <<  9, 'New 4.1 protocol'),
        'INTERACTIVE':        (1 << 10, 'This is an interactive client'),
        'SSL':                (1 << 11, 'Switch to SSL after handshake'),
        'IGNORE_SIGPIPE':     (1 << 12, 'IGNORE sigpipes'),
        'TRANSACTIONS':       (1 << 13, 'Client knows about transactions'),
        'RESERVED':           (1 << 14, 'Old flag for 4.1 protocol'),
        'SECURE_CONNECTION':  (1 << 15, 'New 4.1 authentication'),
        'MULTI_STATEMENTS':   (1 << 16, 'Enable/disable multi-stmt support'),
        'MULTI_RESULTS':      (1 << 17, 'Enable/disable multi-results'),
        'SSL_VERIFY_SERVER_CERT':     (1 << 30, ''),
        'REMEMBER_OPTIONS':           (1 << 31, ''),
    }
    
    default = [
        LONG_PASSWD,
        LONG_FLAG,
        CONNECT_WITH_DB,
        PROTOCOL_41,
        TRANSACTIONS,
        SECURE_CONNECTION,
        MULTI_STATEMENTS,
        MULTI_RESULTS,
    ]

    @classmethod
    def get_default(cls):
        flags = 0
        for f in cls.default:
            flags |= f
        return flags

class ServerFlag(_constantflags):
    """
    Server flags as found in the MySQL sources mysql-src/include/mysql_com.h
    """
    _prefix = 'SERVER_'
    STATUS_IN_TRANS             = 1 << 0
    STATUS_AUTOCOMMIT           = 1 << 1
    MORE_RESULTS_EXISTS         = 1 << 3
    QUERY_NO_GOOD_INDEX_USED    = 1 << 4
    QUERY_NO_INDEX_USED         = 1 << 5
    STATUS_CURSOR_EXISTS        = 1 << 6
    STATUS_LAST_ROW_SENT        = 1 << 7
    STATUS_DB_DROPPED           = 1 << 8
    STATUS_NO_BACKSLASH_ESCAPES = 1 << 9

    desc = {
        'SERVER_STATUS_IN_TRANS':            (1 << 0, 'Transaction has started'),
        'SERVER_STATUS_AUTOCOMMIT':          (1 << 1, 'Server in auto_commit mode'),
        'SERVER_MORE_RESULTS_EXISTS':        (1 << 3, 'Multi query - next query exists'),
        'SERVER_QUERY_NO_GOOD_INDEX_USED':   (1 << 4, ''),
        'SERVER_QUERY_NO_INDEX_USED':        (1 << 5, ''),
        'SERVER_STATUS_CURSOR_EXISTS':       (1 << 6, ''),
        'SERVER_STATUS_LAST_ROW_SENT':       (1 << 7, ''),
        'SERVER_STATUS_DB_DROPPED':          (1 << 8, 'A database was dropped'),
        'SERVER_STATUS_NO_BACKSLASH_ESCAPES':   (1 << 9, ''),
    }

class RefreshOption(_constants):
    """Options used when sending the COM_REFRESH server command."""
    
    _prefix = 'REFRESH_'
    GRANT = 1 << 0
    LOG = 1 << 1
    TABLES = 1 << 2
    HOST = 1 << 3
    STATUS = 1 << 4
    THREADS = 1 << 5
    SLAVE = 1 << 6
    
    desc = {
        'GRANT': (1 << 0, 'Refresh grant tables'),
        'LOG': (1 << 1, 'Start on new log file'),
        'TABLES': (1 << 2, 'close all tables'),
        'HOSTS': (1 << 3, 'Flush host cache'),
        'STATUS': (1 << 4, 'Flush status variables'),
        'THREADS': (1 << 5, 'Flush thread cache'),
        'SLAVE': (1 << 6, 'Reset master info and restart slave thread'),
    }


class ShutdownType(_constants):
    """Shutdown types used by the COM_SHUTDOWN server command."""
    _prefix = ''
    SHUTDOWN_DEFAULT = 0
    SHUTDOWN_WAIT_CONNECTIONS = 1
    SHUTDOWN_WAIT_TRANSACTIONS = 2
    SHUTDOWN_WAIT_UPDATES = 8
    SHUTDOWN_WAIT_ALL_BUFFERS = 10
    SHUTDOWN_WAIT_CRITICAL_BUFFERS = 11
    KILL_QUERY = 254
    KILL_CONNECTION = 255

    desc = {
        'SHUTDOWN_DEFAULT': (0,
            "defaults to SHUTDOWN_WAIT_ALL_BUFFERS"),
        'SHUTDOWN_WAIT_CONNECTIONS': (1,
            "wait for existing connections to finish"),
        'SHUTDOWN_WAIT_TRANSACTIONS': (2,
            "wait for existing trans to finish"),
        'SHUTDOWN_WAIT_UPDATES': (8,
            "wait for existing updates to finish"),
        'SHUTDOWN_WAIT_ALL_BUFFERS': (10,
            "flush InnoDB and other storage engine buffers"),
        'SHUTDOWN_WAIT_CRITICAL_BUFFERS': (11,
            "don't flush InnoDB buffers, "
            "flush other storage engines' buffers"),
        'KILL_QUERY': (254, "(no description)"),
        'KILL_CONNECTION': (255, "(no description)"),
    }


class CharacterSet(_constants):
    """MySQL supported character sets and collations
    
    List of character sets with their collations supported by MySQL. This
    maps to the character set we get from the server within the handshake
    packet.
    
    The list is hardcode so we avoid a database query when getting the
    name of the used character set or collation.
    """
    
    desc = [
      # (character set name, collation, default)
      None,
      ("big5","big5_chinese_ci",True), # 1
      ("latin2","latin2_czech_cs",False), # 2
      ("dec8","dec8_swedish_ci",True), # 3
      ("cp850","cp850_general_ci",True), # 4
      ("latin1","latin1_german1_ci",False), # 5
      ("hp8","hp8_english_ci",True), # 6
      ("koi8r","koi8r_general_ci",True), # 7
      ("latin1","latin1_swedish_ci",True), # 8
      ("latin2","latin2_general_ci",True), # 9
      ("swe7","swe7_swedish_ci",True), # 10
      ("ascii","ascii_general_ci",True), # 11
      ("ujis","ujis_japanese_ci",True), # 12
      ("sjis","sjis_japanese_ci",True), # 13
      ("cp1251","cp1251_bulgarian_ci",False), # 14
      ("latin1","latin1_danish_ci",False), # 15
      ("hebrew","hebrew_general_ci",True), # 16
      None,
      ("tis620","tis620_thai_ci",True), # 18
      ("euckr","euckr_korean_ci",True), # 19
      ("latin7","latin7_estonian_cs",False), # 20
      ("latin2","latin2_hungarian_ci",False), # 21
      ("koi8u","koi8u_general_ci",True), # 22
      ("cp1251","cp1251_ukrainian_ci",False), # 23
      ("gb2312","gb2312_chinese_ci",True), # 24
      ("greek","greek_general_ci",True), # 25
      ("cp1250","cp1250_general_ci",True), # 26
      ("latin2","latin2_croatian_ci",False), # 27
      ("gbk","gbk_chinese_ci",True), # 28
      ("cp1257","cp1257_lithuanian_ci",False), # 29
      ("latin5","latin5_turkish_ci",True), # 30
      ("latin1","latin1_german2_ci",False), # 31
      ("armscii8","armscii8_general_ci",True), # 32
      ("utf8","utf8_general_ci",True), # 33
      ("cp1250","cp1250_czech_cs",False), # 34
      ("ucs2","ucs2_general_ci",True), # 35
      ("cp866","cp866_general_ci",True), # 36
      ("keybcs2","keybcs2_general_ci",True), # 37
      ("macce","macce_general_ci",True), # 38
      ("macroman","macroman_general_ci",True), # 39
      ("cp852","cp852_general_ci",True), # 40
      ("latin7","latin7_general_ci",True), # 41
      ("latin7","latin7_general_cs",False), # 42
      ("macce","macce_bin",False), # 43
      ("cp1250","cp1250_croatian_ci",False), # 44
      None,
      None,
      ("latin1","latin1_bin",False), # 47
      ("latin1","latin1_general_ci",False), # 48
      ("latin1","latin1_general_cs",False), # 49
      ("cp1251","cp1251_bin",False), # 50
      ("cp1251","cp1251_general_ci",True), # 51
      ("cp1251","cp1251_general_cs",False), # 52
      ("macroman","macroman_bin",False), # 53
      None,
      None,
      None,
      ("cp1256","cp1256_general_ci",True), # 57
      ("cp1257","cp1257_bin",False), # 58
      ("cp1257","cp1257_general_ci",True), # 59
      None,
      None,
      None,
      ("binary","binary",True), # 63
      ("armscii8","armscii8_bin",False), # 64
      ("ascii","ascii_bin",False), # 65
      ("cp1250","cp1250_bin",False), # 66
      ("cp1256","cp1256_bin",False), # 67
      ("cp866","cp866_bin",False), # 68
      ("dec8","dec8_bin",False), # 69
      ("greek","greek_bin",False), # 70
      ("hebrew","hebrew_bin",False), # 71
      ("hp8","hp8_bin",False), # 72
      ("keybcs2","keybcs2_bin",False), # 73
      ("koi8r","koi8r_bin",False), # 74
      ("koi8u","koi8u_bin",False), # 75
      None,
      ("latin2","latin2_bin",False), # 77
      ("latin5","latin5_bin",False), # 78
      ("latin7","latin7_bin",False), # 79
      ("cp850","cp850_bin",False), # 80
      ("cp852","cp852_bin",False), # 81
      ("swe7","swe7_bin",False), # 82
      ("utf8","utf8_bin",False), # 83
      ("big5","big5_bin",False), # 84
      ("euckr","euckr_bin",False), # 85
      ("gb2312","gb2312_bin",False), # 86
      ("gbk","gbk_bin",False), # 87
      ("sjis","sjis_bin",False), # 88
      ("tis620","tis620_bin",False), # 89
      ("ucs2","ucs2_bin",False), # 90
      ("ujis","ujis_bin",False), # 91
      ("geostd8","geostd8_general_ci",True), # 92
      ("geostd8","geostd8_bin",False), # 93
      ("latin1","latin1_spanish_ci",False), # 94
      ("cp932","cp932_japanese_ci",True), # 95
      ("cp932","cp932_bin",False), # 96
      ("eucjpms","eucjpms_japanese_ci",True), # 97
      ("eucjpms","eucjpms_bin",False), # 98
      ("cp1250","cp1250_polish_ci",False), # 99
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      ("ucs2","ucs2_unicode_ci",False), # 128
      ("ucs2","ucs2_icelandic_ci",False), # 129
      ("ucs2","ucs2_latvian_ci",False), # 130
      ("ucs2","ucs2_romanian_ci",False), # 131
      ("ucs2","ucs2_slovenian_ci",False), # 132
      ("ucs2","ucs2_polish_ci",False), # 133
      ("ucs2","ucs2_estonian_ci",False), # 134
      ("ucs2","ucs2_spanish_ci",False), # 135
      ("ucs2","ucs2_swedish_ci",False), # 136
      ("ucs2","ucs2_turkish_ci",False), # 137
      ("ucs2","ucs2_czech_ci",False), # 138
      ("ucs2","ucs2_danish_ci",False), # 139
      ("ucs2","ucs2_lithuanian_ci",False), # 140
      ("ucs2","ucs2_slovak_ci",False), # 141
      ("ucs2","ucs2_spanish2_ci",False), # 142
      ("ucs2","ucs2_roman_ci",False), # 143
      ("ucs2","ucs2_persian_ci",False), # 144
      ("ucs2","ucs2_esperanto_ci",False), # 145
      ("ucs2","ucs2_hungarian_ci",False), # 146
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      ("utf8","utf8_unicode_ci",False), # 192
      ("utf8","utf8_icelandic_ci",False), # 193
      ("utf8","utf8_latvian_ci",False), # 194
      ("utf8","utf8_romanian_ci",False), # 195
      ("utf8","utf8_slovenian_ci",False), # 196
      ("utf8","utf8_polish_ci",False), # 197
      ("utf8","utf8_estonian_ci",False), # 198
      ("utf8","utf8_spanish_ci",False), # 199
      ("utf8","utf8_swedish_ci",False), # 200
      ("utf8","utf8_turkish_ci",False), # 201
      ("utf8","utf8_czech_ci",False), # 202
      ("utf8","utf8_danish_ci",False), # 203
      ("utf8","utf8_lithuanian_ci",False), # 204
      ("utf8","utf8_slovak_ci",False), # 205
      ("utf8","utf8_spanish2_ci",False), # 206
      ("utf8","utf8_roman_ci",False), # 207
      ("utf8","utf8_persian_ci",False), # 208
      ("utf8","utf8_esperanto_ci",False), # 209
      ("utf8","utf8_hungarian_ci",False), # 210
    ]

    @classmethod
    def get_info(cls,setid):
        """Retrieves character set information as tuple using an ID
        
        Retrieves character set and collation information based on the
        given MySQL ID.

        Returns a tuple.
        """
        try:
            r = cls.desc[setid]
            if r is None:
                raise
            return r[0:2]
        except:
            raise ProgrammingError("Character set '%d' unsupported" % (setid))

    @classmethod
    def get_desc(cls,setid):
        """Retrieves character set information as string using an ID
        
        Retrieves character set and collation information based on the
        given MySQL ID.

        Returns a tuple.
        """
        try:
            return "%s/%s" % cls.get_info(setid)
        except:
            raise
    
    @classmethod
    def get_default_collation(cls, charset):
      """Retrieves the default collation for given character set
      
      Raises ProgrammingError when character set is not supported.
      
      Returns list (collation, charset, index)
      """
      if isinstance(charset, int):
          try:
              c = cls.desc[charset]
              return c[1], c[0], charset
          except:
              ProgrammingError("Character set ID '%s' unsupported." % (
                charset))
      
      for cid, c in enumerate(cls.desc):
        if c is None:
          continue
        if c[0] == charset and c[2] is True:
          return c[1], c[0], cid
      
      raise ProgrammingError("Character set '%s' unsupported." % (charset))
    
    @classmethod
    def get_charset_info(cls, charset=None, collation=None):
        """Get character set information using charset name and/or collation
        
        Retrieves character set and collation information given character
        set name and/or a collation name.
        If charset is an integer, it will look up the character set based
        on the MySQL's ID.
        For example:
            get_charset_info('utf8',None)
            get_charset_info(collation='utf8_general_ci')
            get_charset_info(47)
        
        Raises ProgrammingError when character set is not supported.

        Returns a tuple with (id, characterset name, collation)
        """
        idx = None
        
        if isinstance(charset, int):
            try:
                info = cls.desc[charset]
                return (charset, info[0], info[1])
            except IndexError:
                ProgrammingError("Character set ID %s unknown." % (charset))
        
        if charset is not None and collation is None:
            info = cls.get_default_collation(charset)
            return (info[2], info[1], info[0])
        elif charset is None and collation is not None:
            for cid, info in enumerate(cls.desc):
                if info is None:
                    continue
                if collation == info[1]:
                    return (cid, info[0], info[1])
            raise ProgrammingError("Collation '%s' unknown." % (collation))
        else:
            for cid, info in enumerate(cls.desc):
                if info is None:
                    continue
                if info[0] == charset and info[1] == collation:
                    return (cid, info[0], info[1])
            raise ProgrammingError("Character set '%s' unknown." % (charset))
        
    @classmethod
    def get_supported(cls):
        """Retrieves a list with names of all supproted character sets
        
        Returns a tuple.
        """
        res = []
        for info in cls.desc:
            if info and info[0] not in res:
                res.append(info[0])
        return tuple(res)

class SQLMode(_constants):
    """MySQL SQL Modes

    The numeric values of SQL Modes are not interesting, only the names
    are used when setting the SQL_MODE system variable using the MySQL
    SET command.

    See http://dev.mysql.com/doc/refman/5.6/en/server-sql-mode.html
    """
    _prefix = 'MODE_'
    REAL_AS_FLOAT = 'REAL_AS_FLOAT'
    PIPES_AS_CONCAT = 'PIPES_AS_CONCAT'
    ANSI_QUOTES = 'ANSI_QUOTES'
    IGNORE_SPACE = 'IGNORE_SPACE'
    NOT_USED = 'NOT_USED'
    ONLY_FULL_GROUP_BY = 'ONLY_FULL_GROUP_BY'
    NO_UNSIGNED_SUBTRACTION = 'NO_UNSIGNED_SUBTRACTION'
    NO_DIR_IN_CREATE = 'NO_DIR_IN_CREATE'
    POSTGRESQL = 'POSTGRESQL'
    ORACLE = 'ORACLE'
    MSSQL = 'MSSQL'
    DB2 = 'DB2'
    MAXDB = 'MAXDB'
    NO_KEY_OPTIONS = 'NO_KEY_OPTIONS'
    NO_TABLE_OPTIONS = 'NO_TABLE_OPTIONS'
    NO_FIELD_OPTIONS = 'NO_FIELD_OPTIONS'
    MYSQL323 = 'MYSQL323'
    MYSQL40 = 'MYSQL40'
    ANSI = 'ANSI'
    NO_AUTO_VALUE_ON_ZERO = 'NO_AUTO_VALUE_ON_ZERO'
    NO_BACKSLASH_ESCAPES = 'NO_BACKSLASH_ESCAPES'
    STRICT_TRANS_TABLES = 'STRICT_TRANS_TABLES'
    STRICT_ALL_TABLES = 'STRICT_ALL_TABLES'
    NO_ZERO_IN_DATE = 'NO_ZERO_IN_DATE'
    NO_ZERO_DATE = 'NO_ZERO_DATE'
    INVALID_DATES = 'INVALID_DATES'
    ERROR_FOR_DIVISION_BY_ZERO = 'ERROR_FOR_DIVISION_BY_ZERO'
    TRADITIONAL = 'TRADITIONAL'
    NO_AUTO_CREATE_USER = 'NO_AUTO_CREATE_USER'
    HIGH_NOT_PRECEDENCE = 'HIGH_NOT_PRECEDENCE'
    NO_ENGINE_SUBSTITUTION = 'NO_ENGINE_SUBSTITUTION'
    PAD_CHAR_TO_FULL_LENGTH = 'PAD_CHAR_TO_FULL_LENGTH'

    @classmethod
    def get_desc(cls, name):
        raise NotImplementedError

    @classmethod
    def get_info(cls, number):
        raise NotImplementedError

    @classmethod
    def get_full_info(cls):
        """Returns a sequence of all availble SQL Modes

        This class method returns a tuple containing all SQL Mode names. The
        names will be alphabetically sorted.

        Returns a tuple.
        """
        res = []
        for key in vars(cls).keys():
            if not key.startswith('_') and not callable(getattr(cls, key)):
                res.append(key)
        return tuple(sorted(res))

