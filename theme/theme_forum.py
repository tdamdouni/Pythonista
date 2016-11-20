# https://gist.github.com/Phuket2/1a55b7cc4dc19df094717db5889c0c1c

# https://forum.omz-software.com/topic/3200/example-editor-present_themed-with-embedded-pyui-loaded-into-a-custom-ui-view

import ui
import base64, bz2, textwrap
import clipboard, editor

# wrapper.py, Pythonista Forum @JonB
# https://forum.omz-software.com/topic/3176/use-a-pyui-file-in-another-pyui-file
# remember to add the the name of the class to the 'Custom View Class'
# in the .pyui

__the_view = \
	'''
QlpoOTFBWSZTWSFRcg4ABLBfgFUQUGd/9T/G3Yq/79/+UAR+6rY6zCHAA7hkQU9NTxTaJH
qTTEx6gAaAmEY0BA1NNGgaRpEBpoAADQAAAASaiVT/U0SGQAADQaPSAGRoGgBzTEyZNGEw
TE0wCYBDBGBGAKkiJinpNMmmkm9UxAAAAAyPUY2qYxNsioB9I1Pb01uvSYUYCgXG4BzA6b
MAYZFgjFBYAoszk1EIiZBDywhjVFFRJkSJ4Xh4VCvZU1MDMArO/6u/td9/fwD4xnOppLee
zliQptjekpRJeGKLLQ28PZ5sKXH94ZW9Orw5/Fjsm7FSgPS7h0Pm2spxEXixysy0a0CpJA
xO5iAFGIwXaqqqq4xiF0JC0MAIYjAoC7urAuxRMVIVAOGXOPu7yoa5LAoCwEA8dUehk3Ut
vbRIdjah2WaIpl0GDyBZxNZRgAUMaQgmvkzc1BuU56qUcaGofmsU6Yle8bN2aRWMJs2jkt
oaTTcuqq1HWcPAp18SDooVAMNBIZY6U0rmhOq5M+F78z82zuptrt4uxheLdUHD8NdqYNDE
QoNGq1pqgTCd+sNaWwsg1VRFQiy1CVywg42OIamUwHBVhVDhQMRqTukJirWCStB3tFpSmq
RvBlZLPSgJCOl8GhzMrzO618nIGgqiklPCZvDcBWKZKYRaUoQIPyyrjK82GdFBoIqjawmS
UqyDsU23TnfgroxsjioVhR5vTLMQndFuN9aRwjZc5zmXwIKuIOVl2WazeKAEguOk1Njp0s
ysemebHNLL1C0tnJi29ZnB6WOfJDfdmpHUz1RtWW0+toZ4yWUhWNI22mNzxBjHVug+QW5Q
wMopyRSTLorRrIcOCf4dB0Xg8A7lIHcUIeEyBBAgcfNzADt3OSG0hOkcYjQ8rm+lDpIH2G
ktYMpDzNuUMip+6V/0KazJeYd7FP9qRUz9jCRhsFkZFNuFsbGM23hh2zKntKkjx6uhbHh/
V6FN79GMNq8LVN19DB62bkby0NzSabk8av01WstItDM1LTxKdvdzhYvqSWYKMpprGbfDxb
uI65+c59J5MJq3zh5OPpmHV3nBOfcqqrvuh9nWwM/LaFbHA5urzzY1lodxS8vYk5z3zTBM
fRLjLp52Uwhsl8pLFStz0dUPPOMwjJvk4sOM42Zd3L9jk3dkoawWye5uJ24LTu3tJL1I0Q
rshxkcip3yG6aX9c5TezLlxtM3GF5rL20hz6jOslZ4s90TOZysDSGnWau2YjE3uvlC78Jb
sR2bu05uHwXidMTGbDi8BQ9RVUqKKUCCOyAdDXvOeADz6csAxJ8/t7+N4m+Lk+nJqzeavC
ERogi9CCIn+LuSKcKEgQqLkHA=
'''

_themes = ['Dawn', 'Tomorrow', 'Solarized Light', 
'Solarized Dark', 'Cool Glow', 'Gold', 'Tomorrow Night', 'Oceanic',
'Editorial']

def pyui_encode(pyui_filename):
	with open(pyui_filename, 'rb') as f:
		pyui = f.read()
		compressed = base64.b64encode(bz2.compress(pyui)).decode('utf-8')
		return '\n'.join(textwrap.wrap(compressed, 70)) 	

def pyui_decode(str):
	s = bz2.decompress(base64.b64decode(str))
	return s.decode('utf-8')

def WrapInstance(obj):
	class Wrapper(obj.__class__):
		def __new__(cls):
			return obj
	return Wrapper
		
class MyClass(ui.View):
	def __init__(self, str,  *args, **kwargs):
		ui.load_view_str(str, bindings={'MyClass': WrapInstance(self), 'self': self})
		super().__init__(*args, **kwargs)
		
if __name__ == '__main__':
	for theme in _themes:
		mc = MyClass( pyui_decode(__the_view), name = theme)
		editor.present_themed(mc, theme_name=theme, style = 'sheet')
		mc.wait_modal()
	
