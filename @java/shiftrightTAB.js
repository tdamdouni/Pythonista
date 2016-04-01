// Add tabs to beginning of selected lines

var indentChar = '\t';

var lnRange = getSelectedLineRange();
var ln = getTextInRange(lnRange[0],lnRange[1]);
var selRange = getSelectedRange();

var lines = ln.split('\n');
var charsAdded = 0;

for (var ix=0; ix < lines.length; ix++) {
  if (lines[ix].length > 0 ) {
    lines[ix] = indentChar + lines[ix];
    charsAdded = charsAdded + indentChar.length;
  }
}

setTextInRange(lnRange[0],lnRange[1],lines.join("\n"));

if (lnRange[0] < selRange[0]) {
  setSelectedRange(selRange[0]+indentChar.length,selRange[1]+charsAdded-indentChar.length);
}
else {
  setSelectedRange(selRange[0]+indentChar.length,selRange[1]+charsAdded);
}

