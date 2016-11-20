# https://forum.omz-software.com/topic/3385/solved-how-to-install-greenlet-for-gevent-websocket/5


from aiobottle import AsyncBottle
import aiohttp

app = AsyncBottle()

@app.get('/')
def root():
	return 'hello word!'
	
def main(host='0.0.0.0', port=8080):
	from bottle import run
	
	run(app, host = host, port = port, server = 'aiobottle:AsyncServer')
	
if __name__ == '__main__':
	main()
# --------------------

