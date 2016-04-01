// http://ole.michelsen.dk/blog/view-source-on-the-ipad-and-iphone.html

javascript:(function(){
  var w = window.open('about:blank'),
      s = w.document;
  s.write('');
  s.close();
  var f = s.body.appendChild(s.createElement('form'));
      f.setAttribute('method','post');
      f.setAttribute('action','http://ole.michelsen.dk/viewsource/?uri='+location.href);
  var i = f.appendChild(s.createElement('input'));
      i.setAttribute('type','hidden');
      i.setAttribute('name','DOM');
      i.setAttribute('value',encodeURIComponent(document.documentElement.innerHTML));
  f.submit();
})();