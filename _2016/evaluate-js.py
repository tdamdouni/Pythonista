# https://gist.github.com/jsbain/85a26b89b01dfe9a488c4bdc6f6827c6

# https://forum.omz-software.com/topic/3773/webview-inspect-element

import ui,console


def show_firebug(w,sender):
	console.hud_alert('button')
	w.eval_js('''
(function(F,i,r,e,b,u,g,L,I,T,E){
	if(F.getElementById(b)){
		// TODO: Figure out how to redisplay debugger
		return;
	}
	E=F[i+'NS'] && F.documentElement.namespaceURI;
	E=E?F[i+'NS'](E,'script'):F[i]('script');
	E[r]('id',b);
	E[r]('src',I+g+T);
	E[r](b,u);
	(F[e]('head')[0]||F[e]('body')[0]).appendChild(E);
	E=new Image;
	E[r]('src',I+L);
})(document,
	'createElement',
	'setAttribute',
	'getElementsByTagName',
	'FirebugLite',
	'4',
	'firebug-lite.js',
	'releases/lite/latest/skin/xp/sprite.png',
	'https://getfirebug.com/',
	'#startOpened');''')
def main():
	b=ui.ButtonItem()
	b.title='Show Debugger'
	b.action=lambda sender:show_firebug(w,sender)
	w=ui.WebView()
	w.load_url('http://getfirebug.com/firebug-lite.js')
	w.right_button_items=b,
	w.present()
	return w
if __name__=='__main__':
	w=main()
