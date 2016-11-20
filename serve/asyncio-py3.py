# https://forum.omz-software.com/topic/3240/asyncio-doesn-t-work-in-pythonista-3

import asyncio

async def hello_world():
	print("Hello World!")
	
loop = asyncio.get_event_loop()
# Blocking call which returns when the hello_world() coroutine is done
loop.run_until_complete(hello_world())
# loop.close()

