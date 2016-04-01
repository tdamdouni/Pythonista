"""Simple awk like program """

"""
todo
  __doc__
  python 3
  multiline
"""

from __future__ import division

import argparse
import fileinput
import os
import re
import sys
import textwrap


class _Tempvar:
    def __init__(self, args):
        self.args = args
        self.ap = ""
        self.ns = ""
        self.line = ""
        self.tmpfile = ""
        self.field = ""
        self.code = ""

    def convert(self, x):
        if x.isdigit():
            return int(x)
        else:
            try:
                return float(x)
            except ValueError:
                return x


def main(_tempvar):
    _tempvar = _Tempvar(_tempvar)
    _tempvar.ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(r'''
    A simple awk like program.
    - Built-in Variables
      SS        crrent record (or line) like $0 in awk
      S         list of fields (s[0], s[1], s[2] like  $1, $2 $3 in awk)
      NR        current record number (or line number) cumulative
      FNR       current record number (or line number) in current file
      FILENAME  current file name
      NF        number of fiels in current recors (same as (len(S))
      - do not use "_tempvar" or "_Tempvar" as a variable
                or as a part of string in scripts

    Examples:
    -  ls -l |simpleawk "if NF > 8 and S[8].endswith('.txt'): print S[8], S[4]"
          - print the text files and theire respective sizes
    -  ls -l |simpleawk -b "sz =0" -e "print 'totel size', sz" "if NF > 8 and
           S[8].endswith('.txt'):\n\tprint S[8], S[4]\n\tsz += sp4]\n"
          - print the  total size in addition to the above information
    -  simpleawk "print SS," file1 file2
          - like cat file1 file2
    -  simpleawk -b "nw=0;nc=0" -e "print NR, nw, nc" "nw+=NF;nc+=len(SS)"
          - like wc file1

    Implementation Notes:
    '''))
    _tempvar.ap.add_argument(
        'SCRIPT', action="store",
        help='the script to process line')
    _tempvar.ap.add_argument(
        'files', nargs='*',
        help='files to be processed')
    _tempvar.ap.add_argument(
        '-b', '--begin', action='store', dest="BEGIN",
        help='script to insert at beginning for initialization')
    _tempvar.ap.add_argument(
        '-e', '--end', action='store', dest="END",
        help='script to insert at end for final processing')
    _tempvar.ap.add_argument(
        '-F', '--fieldseparator', action='store',
        dest="FS", help='field separator')
    _tempvar.ap.add_argument(
        '-d', '--debug', action='store_true',
        help='enable debug')
    _tempvar.ap.add_argument(
        '-head', '--head', action='store',
        help='print first specified lines')
    _tempvar.ap.add_argument(
        '-encoding', '--encoding', action='store',
        help='encoding, default utf8')
    _tempvar.ns = _tempvar.ap.parse_args(_tempvar.args)

    # Do not try to process directories
    _tempvar.ns.files = [
        _tempvar.tmpfile for _tempvar.tmpfile in _tempvar.ns.files if
        not os.path.isdir(_tempvar.tmpfile)]
    fileinput.close()  # in case it is not closed
    if not _tempvar.ns.encoding:
        _tempvar.ns.encoding = 'utf8'
    if _tempvar.ns.BEGIN:
        _tempvar.ns.BEGIN = _tempvar.ns.BEGIN.decode(
            'string-escape').replace("_tempvar", "").replace(
            "_Tempvar", "")
        exec(_tempvar.ns.BEGIN)
    _tempvar.ns.code = compile(_tempvar.ns.SCRIPT.decode(
        'string-escape').replace(
        "_tempvar", "").replace("_Tempvar", ""), '<string>', 'exec')
    if _tempvar.ns.debug:
        print "DEBUG: SCRIPT", _tempvar.ns.SCRIPT
    try:
        for _tempvar.line in fileinput.input(_tempvar.ns.files):
            NR = fileinput.lineno()
            FNR = fileinput.filelineno()
            FILENAME = fileinput.filename()
            SS = unicode(_tempvar.line, _tempvar.ns.encoding)
            if _tempvar.ns.FS:
                S = [_tempvar.convert(
                    _tempvar.field) for _tempvar.field in re.split(
                    _tempvar.ns.FS, SS.rstrip())]
            else:
                S = [_tempvar.convert(
                    _tempvar.field) for _tempvar.field in SS.split()]
            NF = len(S)
            exec(_tempvar.ns.code)
            if _tempvar.ns.debug:
                print "DEBUG:", "NR =", NR, "FNR =", FNR,
                print "FILENAME =", FILENAME, "SS =", SS, "S =", S
            if _tempvar.ns.head:
                if NR == int(_tempvar.ns.head):
                    fileinput.close()
    except Exception as _tempvar.err:
        sys.stderr.write("simpleawk: {}: {!s}".format(
            type(_tempvar.err).__name__, _tempvar.err))
    finally:
        fileinput.close()
    if _tempvar.ns.END:
        _tempvar.ns.END = _tempvar.ns.END.decode(
            'string-escape').replace("_tempvar", "").replace("_Tempvar", "")
        exec(_tempvar.ns.END)

if __name__ == "__main__":
    main(sys.argv[1:])
