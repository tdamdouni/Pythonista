""" cat bin asccii

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
import binascii


def main(args):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('files', nargs='*', help='files to be processed')
    ap.add_argument('-u', '--catunbinascii', action='store_true',
                    help='convert binascii to binary file')
    ap.add_argument('-b', '--buffersize', action='store',
                    help='buffer size')
    ns = ap.parse_args(args)
    if not ns.buffersize:
        ns.buffersize = 32
    else:
        ns.buffersize = int(ns.buffersize)
    files = None
    if not ns.catunbinascii:
        try:
            files = [f for f in ns.files if not os.path.isdir(f)]
            for f in files:
                fp = open(f, "rb")
                buf = fp.read(ns.buffersize)
                while buf:
                    print binascii.hexlify(buf)
                    buf = fp.read(ns.buffersize)
                fp.close()
        except IOError as err:
            sys.stderr.write("catbinascii: {}: {!s}".format(
                type(err).__name__, err))
    else:
        try:
            if ns.files:
                if len(ns.files) == 1:
                    fps = sys.stdin
                    if not os.path.isdir(ns.files[0]):
                        fpd = open(files[1], "wb")
                    else:
                        sys.stderr.write("%s destination file is a directory\n"
                                         % ns.files[0])
                        sys.exit(0)
                elif len(ns.files) == 2:
                    if not os.path.isdir(ns.files[0]):
                        fps = open(ns.files[0])
                    else:
                        sys.stderr.write(
                            "%s source file is a directory\n" % ns.files[0])
                        sys.exit(0)
                    if not os.path.isdir(ns.files[1]):
                        fpd = open(ns.files[1], "wb")
                    else:
                        sys.stderr.write("%s destination file is a directory\n"
                                         % ns.files[1])
                        sys.exit(0)
                else:
                    sys.stderr.write("too many files specified\n")
                    sys.exit(0)
                line = fps.readline()
                while line:
                    fpd.write(binascii.unhexlify(line.strip()))
                    line = fps.readline()
                fps.close()
                fpd.close()
        except IOError as err:
            sys.stderr.write("catbinascii: {}: {!s}".format(
                type(err).__name__, err))


if __name__ == "__main__":
    main(sys.argv[1:])
