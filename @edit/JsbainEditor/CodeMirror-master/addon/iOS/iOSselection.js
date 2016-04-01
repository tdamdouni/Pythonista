/*global CodeMirror, WebKitPoint */
/*jslint plusplus: true, browser: true, vars: true */

/*
iOS CodeMirror Support (C) 2013 Emmanuel Schanzer
 
 Remaining issues:
  - use keyboard height, not wrapperHeight, to determine where to draw the popup
  - magnifier is drawn incorrectly due to onresize event (maybe refactor drawing code?)
  - pasting over some text should hide the selectionDots (maybe refactor drawing code?)
  - handle selection borders ourselves
*/
function iOSselection(cm, enabled) {
  "use strict";
  if(!enabled){ return; }
  // only activate on an iOS device
  if(!(navigator.userAgent.match(/iphone|ipad|ipod/i))){ return false;}
   // set common variables we'll be using
   var clipboardText  = "",
       zoom           = 1.5,
       wrapper        = cm.getWrapperElement(),
       scroller       = cm.getScrollerElement(),
       gutterWidth    = cm.getGutterElement().offsetWidth,
       magnifiedCM    = new CodeMirror(cm.getWrapperElement(),{value: cm.getDoc().linkedDoc()});
   magnifiedCM.setOption("lineNumbers", cm.getOption("lineNumbers"));
   magnifiedCM.getWrapperElement().className += " CodeMirror-focused";
   // programmatically load required stylesheet
   var cssLink  = document.createElement('link');
   cssLink.type = 'text/css';
   cssLink.rel  = 'stylesheet';
   cssLink.href = '../addon/iOS/iOSselection.css';
   cssLink.title= 'iOS Selection CSS Support';
   document.getElementsByTagName('head')[0].appendChild(cssLink);
   // steal Marijnh's beautiful element-creation function (from https://github.com/marijnh/CodeMirror )
   function elt(tag, content, id, className) {
     var e = document.createElement(tag);
     if (className){ e.className = className;}
     if (id){ e.id = id;}
     if (typeof content === "string"){ e.innerHTML=content;}
     else if(content){ for (var i = 0; i < content.length; ++i){e.appendChild(content[i]);}}
     return e;
   }
  
  // provide BoundingClientRect in logical (node) coordinates
  // by converting the top-left and bottom-right points into Node coordinates
  CodeMirror.replaceGetRect(function(elt, pixel_coord){
    var bcr_p = elt.getBoundingClientRect(), // this uses page coordinates
        BR = window.webkitConvertPointFromPageToNode(elt, new WebKitPoint(bcr_p.right, bcr_p.bottom)),
        TL = window.webkitConvertPointFromPageToNode(elt, new WebKitPoint(bcr_p.left, bcr_p.top)),
        bcr_l = {left: TL.x, top: TL.y, right: BR.x, bottom: BR.y, height: BR.y-TL.y, width: BR.x-TL.x};
    return pixel_coord? bcr_p : bcr_l;
  });

   // create various DOM elements we'll be using, and append selectionDots to the scroller
   var selectAll= elt('li', "Select All"), select = elt('li', "Select"), paste = elt('li', "Paste"),
       copy     = elt('li', "Copy"), cut = elt('li', "Cut"),
       startSel = elt('span',[elt('span')],'start','selectionDotTouchTarget'),
       endSel   = elt('span',[elt('span')],'end','selectionDotTouchTarget'),
       popup    = elt('ul',null,'iOSpopup'),
       magnifiedStuff = elt('div',[magnifiedCM.getWrapperElement()],null,'magnifiedStuff'),
       magnifier= elt('div',[magnifiedStuff],'magnifier'),
       notch    = elt('b',null,'notch','above'),
       tool     = elt('div',[popup,magnifier,notch],'tool');
   magnifiedStuff.style.webkitTransform = "scale("+zoom+")";
   scroller.firstChild.firstChild.appendChild(startSel); // LIKELY TO BREAK IF CM'S DOM CHANGES
   scroller.firstChild.firstChild.appendChild(endSel);   // LIKELY TO BREAK IF CM'S DOM CHANGES
   // Make sure there's only one tool node on the page
   if(!document.getElementById('tool')){document.body.appendChild(tool);}
   
   // place the dots using local coordinates, or hide them altogether if nothing is seleced
   function drawSelectionDots(){
     var selected  = cm.somethingSelected(),
         start = cm.cursorCoords(true, "local"),
         end = cm.cursorCoords(false,"local");
     startSel.style.display = endSel.style.display = selected? 'block' : 'none';
     startSel.style.left = start.left + "px"; startSel.style.top  = start.top  + "px";
     endSel.style.left   = end.left   + "px"; endSel.style.top    = end.bottom + "px";
   }
   // given a touch event and an optional (x,y) coord, draw the relevant tool
   function drawTool(e, x, y){
      var selected    = cm.somethingSelected(),
          landscape   = Math.abs(window.orientation) === 90,
          deviceWidth = landscape? Math.max(480, screen.height) : screen.width,
          deviceScale = window.innerWidth/deviceWidth,
          popupX;
      // draw the Magnifier and position the notch
      function drawMagnifier(){
         magnifier.className = !selected? "circle" : "rectangle";
         magnifiedCM.scrollTo(cm.getScrollInfo().left, cm.getScrollInfo().top);
         tool.style.left = x - tool.offsetWidth/2 + "px";
         tool.style.top  = y - magnifier.offsetHeight - (selected? 30 : 0) + "px";
         magnifiedStuff.style.left = (-x-cm.getScrollInfo().left+wrapper.offsetLeft)*zoom+magnifier.offsetWidth/2+"px";
         magnifiedStuff.style.top  = (-y+wrapper.offsetTop+magnifier.offsetHeight/6)*zoom+"px";
         notch.style.left = -tool.offsetWidth/2 - notch.offsetWidth/2 + 'px'; // shift left by half notchWidth
         notch.className ='above';
      }
      // draw the Popup using page coordinares, and position the notch
      function drawPopup(){
        var start = cm.cursorCoords(true, "page"), end = cm.cursorCoords(false, "page");
        if(selected){
           popup.appendChild(cut); popup.appendChild(copy);
           popupX = (start.top===end.top)? (start.left+end.left)/2 : (scroller.offsetLeft+wrapper.offsetWidth)/2;
         } else {
           if(cm.getValue().length > 0){ popup.appendChild(select); popup.appendChild(selectAll);}
           popupX = start.left;
         }
         if(clipboardText.length>0){ popup.appendChild(paste);}
         // Assume the popup is centered onscreen, notch pointing down. Then check edge cases and notch direction.
         notch.className ='above';
         tool.style.top  = wrapper.offsetTop + wrapper.offsetHeight/2 + "px";
         if(start.top > wrapper.offsetTop && start.top-tool.offsetHeight > window.pageYOffset){
           tool.style.top  = start.top - (tool.offsetHeight+10) + "px";
         } else if (end.bottom+tool.offsetHeight+10 < wrapper.offsetTop+wrapper.offsetHeight){
           notch.className='below';
           tool.style.top = end.bottom+10*deviceScale+"px";
         }
         // make sure the popup is never out of bounds, and position the triangle near cursor with CSS
         var tw = tool.offsetWidth;
         tool.style.left = Math.min(Math.max(gutterWidth, popupX-tw/2), deviceWidth-tw) + "px";
         notch.style.left  = Math.min(Math.max(15, popupX-tool.offsetLeft), tw-15)-tw-10+"px";
      }
      // scale all of our faked elements, so they appear constant in the face of user-zoom
      tool.style.webkitTransform = "scale("+deviceScale+")";
      endSel.style.webkitTransform=startSel.style.webkitTransform = "scale("+deviceScale+")";
      // position selectionDots, empty and reset the popup, and draw the appropriate tool
      drawSelectionDots(e);
      popup.innerHTML = null; tool.style.left = '0px';
      if(tool.className==="magnify"){ drawMagnifier(e); }
      if(tool.className==="popup")  { drawPopup(e);     }
    }
   // Factory: capture the event, prevent default, execute f, and redraw the popup
   function popupFactory(f){return function(e){cm.focus(); e.stopPropagation(); e.preventDefault(); f(e); drawTool(e);};}

   // Factory: return methods for changing CM start and end cursors, which also control magnifier display
   function updateCursors(mode){
     return function(e){
         e.stopPropagation(); e.preventDefault();
         // switch the tool class based on touchevent type (touchend->magnify, everything else->popup)
         tool.className = (e.type !== 'touchend')? "magnify" : "popup";
         var adjustY  = (mode!=="end")? startSel.firstChild.offsetHeight : -endSel.firstChild.offsetHeight;
         e.coords     = {left: e.changedTouches[0].pageX,
                         top: e.changedTouches[0].pageY+(mode==="both"? 0 : adjustY)};
         var startPos = (mode!=="end")?   cm.coordsChar(e.coords) : cm.getCursor(true),
             endPos   = (mode!=="start")? cm.coordsChar(e.coords) : cm.getCursor(false);
         // if the cursor positions are valid, update selection in both CMs, and scroll the editor
         if(mode==="both" || startPos.line<endPos.line || (startPos.line===endPos.line && startPos.ch<endPos.ch)){
            cm.setSelection(startPos, endPos);
            cm.scrollIntoView((mode!=="end"? startPos : endPos));
           if(tool.className == "magnify") {magnifiedCM.setSelection(startPos, endPos);}
         }
         if(tool.className==="magnify" && mode!=="both"){e.coords = cm.cursorCoords(mode==="start");}
         drawTool(e, e.coords.left, e.coords.top+3);
      };
   }
  // POPUP BUTTONS
   function selectAllHandler(){ cm.setSelection({line: 0, ch: 0}, {line: cm.lineCount() - 1}); }
   function copyHandler(){ clipboardText = cm.getSelection(); tool.className = ''; }
   function pasteHandler(){ cm.replaceSelection(clipboardText); tool.className = ''; }
   function cutHandler(){ clipboardText = cm.getSelection(); cm.replaceSelection(""); tool.className = ''; }
   function selectHandler(){
      var start=0, end=0, i=0, cursor = cm.getCursor(),
          words  = cm.getLine(cursor.line).split(/[\s+\(\)\"\']/);
      for(i=0; i < words.length; i++){
        start = end; end+=words[i].length+1;
        if (end>cursor.ch){ break;}
      }
      // if we've got something to select, select it!
      if(start < end-1){
         cm.setSelection({line: cursor.line, ch: start}, {line: cursor.line, ch: end-1});
      // there's only whitespace after the cursor. Step backwards if the line has text, and try selection again
      } else if(start > 0){
        cm.setCursor({line: cursor.line, ch: start-1});
        selectHandler();
      // we're on an empty line. Walk forwards until we find a non-empty line, then select starting whitespace
      } else {
        var endLine = cursor.line;
        while(endLine<cm.lineCount() && cm.getLine(endLine).length===0){ endLine++;}
        var endCh = cm.getLine(endLine).split(/\S/)[0].length;
        cm.setSelection({line: cursor.line, ch: start}, {line: endLine, ch: endCh});
      }
      tool.className = 'popup';
   }
   // set touchMove and touchEnd events, which are cleaned up on touchEnd
   function magnifyCursor(e){
     if(document.activeElement !== cm.getInputField()){cm.focus();}
     var touchMoveListener = updateCursors("both");
     var touchEndListener = function(e){
       tool.className = 'popup';
       updateCursors("both")(e);
       scroller.removeEventListener("touchmove", touchMoveListener, true);
       scroller.removeEventListener("touchend",  touchEndListener,  true);
     };
     scroller.addEventListener("touchmove", touchMoveListener, true);
     scroller.addEventListener("touchend",  touchEndListener,  true);
     // update the cursor and magnifier position
     updateCursors("both")(e);
   }
 /*****************************************************************************************
  *    Connect Event Handlers                                                           */
   var holdTimer = null, recentTap = false, LAST_TOUCH;
   // stop waiting for a tap-hold, and draw the necessary tool nodes
   function moveHandler(e){
     window.clearTimeout(holdTimer);
     LAST_TOUCH = e;
   }
   function endHandler(e){
     window.clearTimeout(holdTimer);
     if(LAST_TOUCH.type === "touchstart"){
       // onDoubleTap: initialize the magnifier, set the cursor to tap location, select and focus
       if(recentTap){
         updateCursors("both")(e);
         popupFactory(selectHandler)(e);
       // onTap: hide selectionDots, and start timer for doubleTap
       } else {
         startSel.style.display=endSel.style.display='none';
         recentTap=window.setTimeout(function(){recentTap=false;},250);
       }
     }
     // make sure the popup returns if something is selected
     if(LAST_TOUCH.type === "touchmove" && cm.somethingSelected()){
        tool.className = 'popup';
        drawTool(e);
     }
     LAST_TOUCH = e;
   }
   // Start the timer for Tap, DoubleTap and Hold events
  function startHandler(e){
     if(e.target.nodeName === "LI"){return;}  // ignore touches to popup buttons
     tool.className = '';
     holdTimer = window.setTimeout(function(){cm.focus();magnifyCursor(e);},250);
     LAST_TOUCH = e;
   }
   // touch events for tapping, double-tapping, tap-holding and scrolling
   CodeMirror.on(scroller,  "touchstart", startHandler);
   CodeMirror.on(scroller,  "touchmove",  moveHandler);
   CodeMirror.on(scroller,  "touchend",   endHandler);
   CodeMirror.on(scroller,  "scroll",     drawTool);
   // selection adjustment handlers
   CodeMirror.on(startSel,  "touchstart", updateCursors("start"));
   CodeMirror.on(endSel,    "touchstart", updateCursors("end"));
   CodeMirror.on(startSel,  "touchmove",  updateCursors("start"));
   CodeMirror.on(endSel,    "touchmove",  updateCursors("end"));
   CodeMirror.on(startSel,  "touchend",   updateCursors("start"));
   CodeMirror.on(endSel,    "touchend",   updateCursors("end"));
   // connect handlers for iOSpopup buttons
   CodeMirror.on(select,    "touchend",   popupFactory(selectHandler));
   CodeMirror.on(selectAll, "touchend",   popupFactory(selectAllHandler));
   CodeMirror.on(cut,       "touchend",   popupFactory(cutHandler));
   CodeMirror.on(copy,      "touchend",   popupFactory(copyHandler));
   CodeMirror.on(paste,     "touchend",   popupFactory(pasteHandler));
   // handle scaling and resizing: draw everything over again
   window.addEventListener("resize",       drawTool);
   window.addEventListener("scroll",       drawTool);
   cm.on("change", function(e){tool.className=''; drawTool(e);});
   return;
}

CodeMirror.defineOption("iOSselection", false, iOSselection);