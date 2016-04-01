# coding: utf-8

# https://forum.omz-software.com/topic/2388/help-with-ui-segment-bar

import ui
import console

def segment1(sender):
    console.alert('Segment 1 Has been selected')

def segment2(sender):
    console.alert('Segment 2 Has been selected')

def segment_action(sender):
    seg_name = sender.segments[sender.selected_index]
    console.alert(seg_name + ' has been selected')
    
def segment_action(sender):
    selection = sender.selected_index
    if selection == 0:
        segment1(sender)
    elif selection == 1:
        segment2(sender)

view = ui.View()
segview = ui.SegmentedControl()
segview.segments = ['seg1', 'seg2']
segview.action = segment_action
view.add_subview(segview)
view.present()

@ui.in_background
def popup():
    console.alert("hello")
popup()