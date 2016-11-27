# https://gist.github.com/Mr-Coxall/e0ca128bb2e7997b6030a50f09323099

# Created by: Mr. Coxall
# Created on: Aug 2016
# Created for: ICS3U
# This program displays area and perimeter of a rectangle,
# but this time the user can enter different lengths and widths

import ui

def calculate_area(length_sent, width_sent):
    # calculate area
    
    area = length_sent * width_sent
    view['area_answer_label'].text = 'The area is: ' + str(area) + ' cm^2'

def calculate_perimeter(length_sent, width_sent):
    # calculate perimeter
    
    perimeter = 2 * (length_sent + width_sent)
    view['perimeter_answer_label'].text = 'The perimeter is: ' + str(perimeter) + ' cm'

def calculate_button_touch_up_inside(sender):
    # calculate area and perimeter
    
    # input
    length = int(view['length_textbox'].text)
    width = int(view['width_textbox'].text)
    
    calculate_area(length, width)
    calculate_perimeter(length, width)

    
view = ui.load_view()
view.present('full_screen')
