# https://forum.omz-software.com/topic/1239/extracting-the-date-from-the-ui-date-and-time-spinner

def GetDate(sender):
  date = sender.superview['DatePicker1']
  # assuming that is the name of your DatePicker object
  # this returns a datetime.datetime object, see module datetime
  year = date.year
  month = date.month
  # etc... For day, hour, minute and so forth.
# --------------------
import ui

my_date = None 

def date_picker_action(sender):
    my_date = sender.date
    print(my_date)

view = ui.View()
date_picker = ui.DatePicker()
date_picker.action = date_picker_action
view.add_subview(date_picker)
view.present('sheet')
# --------------------
def calndr(sender):
  date = sender.superview['calender']
  # assuming that is the name of your DatePicker object
  # this returns a datetime.datetime object, see module datetime
  year = date.year
  month = date.month
  
  with open('newfile.csv',"a") as f:
            newfileWriter=csv.writer(f)
            newfileWriter.writerow([calndr()])
            tarDate=calndr(targetDate['calender'])
            f.close()
# --------------------
def calndr(sender):
    date = sender.superview['calender']
    # assuming that is the name of your DatePicker object
    # this returns a datetime.datetime object, see module datetime
    year = date.year
    month = date.month
    
    with open('newfile.csv', 'a') as csvfile:
        fieldnames = ['Year', 'Month']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Year': year, 'Month': month})
# --------------------
