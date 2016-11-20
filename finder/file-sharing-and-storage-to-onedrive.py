# coding: utf-8

# https://forum.omz-software.com/topic/2719/file-sharing-and-storage-to-onedrive/5

It's relatively easy to get this functionality back. Here's how:

Create a new script, and call it something like "Open in"
Paste the following code:
import console, editor
console.open_in(editor.get_path())
Tap the "wrench" icon
Tap Edit inside the "wrench" menu, then the (+) button that appears
Optionally select a nice icon and color for your action
Tap Done
A "Copy to OneDrive" option should appear in the menu that pops up when you select the new editor action you created.

