import pypi
import os

nltk_data_path = os.path.join("~", "Documents", "nltk_data")
linenum        = 75
data_path      = os.path.join(pypi.installdir, "nltk", "data.py")
hackline       = (" path.append("
                  "os.path.expanduser("
                  "str('{}')))").format(nltk_data_path)

data, url = pypi.download("nltk")
pypi.install(data, url.split("/")[-1], "nltk")

with open(data_path) as in_file:
    lines = in_file.read().splitlines()

lines[linenum - 1] = hackline

with open(data_path, "w") as fp:
    fp.write(os.linesep.join(lines))

full = os.path.expanduser(nltk_data_path)
if not os.path.exists(full):
    os.mkdir(full)
