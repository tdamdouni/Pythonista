import requests
import pypi

link = "https://github.com/PacketPerception/pychievements/archive/master.zip"
data = requests.get(link).content

pypi.install(data, "master.zip", "pychievements/")
