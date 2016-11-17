""" paste - merge corresponding or subsequent lines of files

Examples:

"""

"""
todo:
  __doc__
  test examples
"""

import argparse
import fileinput
import os
import re
import sys


def getline_from_stdin(ns):
    if ns.stdin_eof:
        return ""
    try:
        s = raw_input()
    except EOFError:
        s = ""
        ns.stdin_eof = True
    return s


def main(args):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('files', nargs='*', help='files to be processed')
    ap.add_argument('-d', '--delimiter', action='store',
                    help='use the specified delimiter instead of TABs')
    ap.add_argument('-s', '--serial', action='store_true',
                    help='append the data in serial rather than in parallel')
    ns = ap.parse_args(args)
    ns.stdin_eof = False
    if not ns.delimiter:
        ns.delimiter = "\t"
    files = None
    if not ns.serial:
        try:
            files = [open(f) if f != "-" else None for f in ns.files if (
                f == "-") or (not os.path.isdir(f))]
            lines = []
            while True:
                lines = [fp.readline().rstrip() if fp else getline_from_stdin(
                    ns) for fp in files]
                if all([not i for i in lines]):
                    break
                print (ns.delimiter).join(lines)
        except IOError as err:
            sys.stderr.write("paste: {}: {!s}".format(type(err).__name__, err))
        finally:
            if files:
                for fp in files:
                    if fp:
                        fp.close()
    else:
        try:
            files = [open(f) if f != "-" else None for f in ns.files]
            lines = [fp.read() if fp else sys.stdin.read() for fp in files]
            splitlines = [ns.delimiter.join(
                line.split("\n")) for line in lines]
            for line in splitlines:
                print line
        except IOError as err:
            sys.stderr.write("paste: {}: {!s}".format(type(err).__name__, err))
        finally:
            if files:
                for fp in files:
                    if fp:
                        fp.close()


if __name__ == "__main__":
    main(sys.argv[1:])
