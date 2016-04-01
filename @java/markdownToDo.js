// Prefix selected lines with Markdown to-do checkboxes
// A plain Markdown checkbox, unckecked:
var prefix = "- [ ] ";

var lineRange = getSelectedLineRange();
var ln = getTextInRange(lineRange[0], lineRange[1]);
var selectedRange = getSelectedRange();

function chkLine(line) {
  // These regexp match various checkbox states
  chkd = /^(\s*[-*+]\s)\[x]/i      // checked: "- [x]"
  unchkd = /^(\s*[-*+]\s)\[\s?]/   // unchecked: "- [ ]"
  li = /^(\s*[-*+]\s)/             // list item: "- "

  added = 0;
  if (chkd.test(line)) {
    line = line.replace(chkd, "$1[ ]");
  }
  else if (unchkd.test(line)) {
    line = line.replace(unchkd, "$1[x]");
  }
  else if (li.test(line)) {
    line = line.replace(li, "$1[ ] ");
    added = 4;
  } else {
    line = prefix + line;
    added = 6;
  }
  return {
    text: line,
    added: added
  }
}


if (ln && ln != "") {
  var lines = ln.split('\n');
  var charsAdded = 0;

  for (var ix=0; ix < lines.length; ix++) {
    if (lines[ix].length > 0) {
      line = chkLine(lines[ix]);
      lines[ix] = line.text;
      charsAdded += line.added;
    }
  }

  // Replace text in draft
  setTextInRange(lineRange[0], lineRange[1],lines.join("\n"));


  // Reset selection
  if (lines.length > 2) {
    setSelectedRange(lineRange[0]+lineRange[1]+charsAdded, 0);
  }
  else {
    setSelectedRange(selectedRange[0]+charsAdded, selectedRange[1]);
  }

}
else {
  // If the current line is blank, just add a checkbox
  setSelectedText(prefix);
  charsAdded = prefix.length;
  setSelectedRange(selectedRange[0]+charsAdded, 0);
}