// Outdent lines by removing initial tabs

var indentChar = '\t';

var lnRange = getSelectedLineRange();
var ln = getTextInRange(lnRange[0],lnRange[1]);
var selRange = getSelectedRange();

var lines = ln.split('\n');
var charsRemoved = 0;
var firstLineIndent = true;

for (var ix=0; ix < lines.length; ix++) {
  if (lines[ix].length > 0) {
    if (lines[ix].indexOf(indentChar) == 0) {
      lines[ix] = lines[ix].slice(indentChar.length,lines[ix].length-indentChar.length+1);
      charsRemoved = charsRemoved + indentChar.length;
    }
    else {
      if (ix == 0) {
        firstLineIndent = false;
      }
    }
  }
}

setTextInRange(lnRange[0],lnRange[1],lines.join("\n"));

var startAdj = 0;
if (firstLineIndent) {
  startAdj = indentChar.length;
}

if (lnRange[0] < selRange[0]) {
  setSelectedRange(selRange[0]-startAdj,selRange[1]-charsRemoved+indentChar.length);
}
else {
  setSelectedRange(selRange[0]-startAdj,selRange[1]-charsRemoved);
}
