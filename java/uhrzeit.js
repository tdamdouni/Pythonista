var now = new Date();
var hh =now.getHours();
var mm = now.getMinutes();

if(hh<10) {
    hh='0'+hh
}

if(mm<10) {
    mm='0'+mm
} 

var time = hh+':'+mm;
var selRange = getSelectedRange();
setSelectedText(time);
setSelectedRange(selRange[0]+9,0);