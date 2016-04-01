// Moves cursor to end of draft; inserts date and time; inserts new lines to start typing your log notes. Hack of other scripts in Drafts directory. 

// Move cursor to end of draft

var t = getText();
var g = t.length;
setSelectedRange(g, 0);

// Insert yyyy-mm-dd hh:min

var now = new Date();
var hh = now.getHours();
var min = now.getMinutes();
var dd = now.getDate();
var mm = now.getMonth()+1;
var yyyy = now.getYear()+1900;

if(dd<10) {
    dd='0'+dd
} 

if(mm<10) {
    mm='0'+mm
} 

var today = yyyy+'-'+mm+'-'+dd+' ';
var selRange = getSelectedRange();
setSelectedText(today);
setSelectedRange(selRange[0]+today.length,0);

if(hh<10) {
    hh='0'+hh
}

if(min<10) {
    min='0'+min
} 

var time = hh+':'+min+'\n\n';
var selRange = getSelectedRange();
setSelectedText(time);
setSelectedRange(selRange[0]+9,0);
