https://forum.omz-software.com/topic/1239/extracting-the-date-from-the-ui-date-and-time-spinner/29

import ui
from os.path import exists 
import csv

_csv_filename = 'myoutputV2.csv'
        
def calc_button_action(sender):
    '''
        Here your calc button will call 3 functions.
        1. do_calculations, so you calculate and put the values in your fields
        2. collect_data, will collect all the data from your view and return it as a list
        3. write_to_csv, you pass your list you collected the data into and it will be written
        to the csv file.  The file name is at the top of the file.  You could ask for the name
        of the file for example.
    '''
    
    # v is set to your view, so you can access the other objects on you view now and
    # pass your view to other functions!
    v = sender.superview
    
    do_calculations(v)
    data_list = collect_data(v)
    write_to_csv(_csv_filename, data_list , ['Year', 'Month', 'Day', 'HighPrice'])
    
def do_calculations(v):
    '''
        in here, just do your calculations and update
        your fields with the calculated data
    '''
    # so to access the date in the ui.DatePicker, lets say its name is cal
    the_date = v['cal'].date
    
    # you can access all your objects as above.
    
    v['txt9'].text = str(10 * 2) # whatever you calculate
    
    
def collect_data(v):
    '''
        in here you are only intrested in collecting your data from the view
        again, you have the view so you can access your fields.
        Using a list now! not a dict
    '''
    lst = []
    # I have only filled in a few fields here. But you would add everything from your view
    # you wanted written out to the csv.  Add the items in the order you want them written 
    # to the csv file.
    lst.append(v['cal'].date.year)
    lst.append(v['cal'].date.month)
    lst.append(v['cal'].date.day)
    lst.append(v['txt9'].text)
    
    return lst
    
def write_to_csv(filename, data_list, field_name_list=None):
    '''
        This function is only concerned with writing your list to the csv file.  
    '''
    fexists=exists(filename) # We set a var to see if the file exists
    
    
    with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        if not fexists and field_name_list != None:
            csvwriter.writerow(field_name_list)
            
        csvwriter.writerow(data_list)   
        
if __name__ == '__main__':
    my_screen_fn = 'someview.pyui'
    v = ui.load_view(my_screen_fn)
    v.present(style='sheet', animated=False)