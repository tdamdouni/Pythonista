import pypi
import os

data, url = pypi.download("networkx")
pypi.install(data, url.split("/")[-1], "networkx")

data, url = pypi.download("decorator")
pypi.install(data, url.split("/")[-1], os.path.join("src", "decorator.py"))
