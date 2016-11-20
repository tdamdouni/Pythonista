# coding: utf-8

# https://forum.omz-software.com/topic/2775/cloud-module/13

import json

with open("modules.json", "r") as f:
	modules = json.load(f)
	
{
    "pythonista": "https://github.com/The-Penultimate-Defenestrator/Pythonista-Tweaks",
    "pythonista.app": "https://github.com/The-Penultimate-Defenestrator/Pythonista-Tweaks",
    "pythonista.editor": "https://github.com/The-Penultimate-Defenestrator/Pythonista-Tweaks",
    "pythonista.console": "https://github.com/The-Penultimate-Defenestrator/Pythonista-Tweaks",
    "Gestures": "https://github.com/mikaelho/pythonista-gestures"
}

import requests

modules = requests.get("https://example.com/modules.json").json

