import aiohttp, asyncio, async_timeout
import ui

class AsyncUIView(ui.View):
  def __init__(self, *args, poll_interval=0.5, **kwargs):
    super().__init__(*args, **kwargs)
    self.running = True
    self.poll_interval = poll_interval
    self.loop = asyncio.get_event_loop_policy().new_event_loop()
    self.task = None
    self._session = aiohttp.ClientSession(loop=self.loop)
    
  def start_loop(self):
    self.loop.run_until_complete(self._runner())
  
  def will_close(self):
    self.running = False
    self._session.close()
    
  async def _runner(self):
    while self.running:
      if self.task:
        task = self.task
        self.task = None
        await task()
      task = self.loop.create_task(asyncio.sleep(self.poll_interval))
      await task
      
  async def get(self, url):
    with async_timeout.timeout(10):
      async with self._session.get(url) as response:
        return await response.text()
  
if __name__ == '__main__':
  
  class CounterButton(ui.View):
    def __init__(self, controller, webview, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.controller = controller
      self.webview = webview
      self.counter = 0
      self.btn = btn = ui.Button(flex='WH', frame=self.bounds, tint_color=(.77, .22, .03), action=self.do_fetch)
      self.add_subview(btn)
      self.update_interval = 0.5
    
    def update(self):
      self.counter += 1
      self.btn.title = f'#{self.counter} - Click me'
      
    def do_fetch(self, sender):
      self.webview.load_html('<span style="font-size: xx-large;">Loading...</span>')
      self.controller.task = self.load_the_page
      
    async def load_the_page(self):
      html = await self.controller.get('http://python.org')
      self.webview.load_html(html)
    
  v = AsyncUIView()
  v.present('full_screen')
  
  w = ui.WebView(frame=v.bounds)
  v.add_subview(w)
  
  b = CounterButton(v, w, frame=v.bounds)
  v.add_subview(b)
  
  v.start_loop()

