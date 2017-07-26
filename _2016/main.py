# https://github.com/tlinnet/hotspotsystem/blob/master/api/pythonista/main.py

###############################################################################
#                                                                             #
#                           Hotspotsystem Vouchers                            #
#                                                                             #
#               View current free vouchers and create new vouchers            #
#                                                                             #
#                             by Troels Schwarz-Linnet                        #
#                                                                             #
###############################################################################
#                                                                             #
#                                   Licence                                   #
#                                                                             #
# Copyright (C) 2016  Troels Schwarz-Linnet, Denmark                          #
#                                                                             #
# Contact: tlinnet *at* gmail dot com                                         #
#                                                                             #
# Available at:                                                               #
# https://github.com/tlinnet/hotspotsystem/tree/master/api/pythonista         #
#                                                                             #
#  Inspired by: https://github.com/khilnani/pythonista-scripts/blob/          #
#  master/thirdparty/UI/ui-tutorial/Three-Column-Sortable-TableView.py        #
#                                                                             #
#                                                                             #
# This program is free software; you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU Library General Public License for more details.                        #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program; if not, write to the Free Software                 #
#                                                                             #
###############################################################################
import os, datetime, json, requests
from operator import itemgetter
from time import strftime

# From: 
# https://github.com/khilnani/pythonista-scripts/blob/master/thirdparty/UI/ui-tutorial/Three-Column-Sortable-TableView.py
# http://omz-software.com/pythonista/docs/ios/ui.html
# http://omz-software.com/pythonista/docs/ios/console.html

# See hotspotsystem API options at: 
# http://www.hotspotsystem.com/apidocs-v1
# http://www.hotspotsystem.com/apidocs/api/reference

##########################################
# file locations used by the program
PYTHONISTA_DOC_DIR = os.path.expanduser('~/Documents')
SYNC_FOLDER_NAME = '.hotspotsystem'
SYNC_STATE_FOLDER = os.path.join(PYTHONISTA_DOC_DIR, SYNC_FOLDER_NAME)
CONFIG_FILENAME = 'hotspotsystem.conf'
CONFIG_FILEPATH = os.path.join(SYNC_STATE_FOLDER, CONFIG_FILENAME)
##########################################

# Switch before last Xcode compiling and Apple submit.

# Check if pythonista
global ispythonista
#ispythonista = False
ispythonista = True

# Check platform
if not ispythonista:
    import platform

    if platform.system() == 'Darwin':
        if platform.machine().startswith('iP'):
            ispythonista = True

        else:
            print('You are running on Mac OS X! %s - %s'%(platform.system(), platform.machine()))
            import logging, sys

            # Custom logging level
            FINE = 15

            # Silence request
            logging.getLogger("requests").setLevel(logging.WARNING)
            logging.getLogger("urllib3").setLevel(logging.WARNING)

            # Process any supplied arguments
            log_level = 'INFO'

            global update_config
            update_config = False

            for argument in sys.argv:
                if argument.lower() == '-v':
                    log_level = 'FINE'
                elif argument.lower() == '-vv':
                    log_level = 'DEBUG'
                elif argument.lower() == '-c':
                    update_config = True

            # configure logging
            log_format = "%(message)s"
            logging.addLevelName(FINE, 'FINE')

            for handler in logging.getLogger().handlers:
                logging.getLogger().removeHandler(handler)
            logging.basicConfig(format=log_format, level=log_level)


            # Python 3 compatibility, for input in terminal
            try: 
    	        input = raw_input
            except NameError:
    	        pass
    else:
        print('Please upgrade to a real computer and then press any key to continue...')

# If pythonista, then import
if ispythonista:
    import ui, console, dialogs
    from objc_util import *

    console.clear()
    # Disable dimming the screen
    console.set_idle_timer_disabled(True)


# Define Class for shared functions
class Common(object):
    def __init__(self):
        self.setup_configuration()

    # If a configuration file does not exist, this will prompt the user for inital configuration values		
    def setup_configuration(self):
        if not os.path.exists(SYNC_STATE_FOLDER):
            os.mkdir(SYNC_STATE_FOLDER)
        if os.path.exists(CONFIG_FILEPATH):
            with open(CONFIG_FILEPATH, 'r') as config_file:
                config = json.load(config_file)
                config['reset'] = False
        else:
            if not ispythonista:
                logging.log(FINE, 'Configuration file missing')

            # Make empty settings dict.
            config = {}

        list_configs = [
        ['limit', "100"],
        ['offset', "0"],
        ['last_voucher', ""],
        ['last_voucher_time', ""],
        ['reset', True],
        ['error_message', None],
        ['success', None],
        ['package_filter', ""],
        ['reset_code', "1234"]
        ]

        # Set key and value if missing in config dict
        for key, val in list_configs:
            if key not in config:
                config[key] = val

        # Store
        self.config = config
        # Write the config file back
        self.write_configuration()

    # Read vouchers from config dict
    def read_vouchers(self, full=False):
        if 'stored_vouchers' in self.config:
            if full:
                return self.config['stored_vouchers']
            else:
                sublist = [item[:3] for item in self.config['stored_vouchers']]
                return sublist
        else:
            self.get_vouchers()
            success = self.get_config(key='success')
            if success:
                if full:
                    return self.config['stored_vouchers']
                else:
                    sublist = [item[:3] for item in self.config['stored_vouchers']]
                    return sublist
            else:
                return []

    # Use hotspotsystem API to get all unused vouchers
    def get_vouchers(self):
        root='https://api.hotspotsystem.com/v1.0'
        url=root+'/locations/'+self.config['LOC_ID']+'/vouchers.json'
        params = {'limit':self.config['limit'],'offset':self.config['offset']}
        r = requests.get(url, auth=(self.config['API_KEY'], 'x'), params=params)
        vouchers = []
        i = 0

        # Get search_criteria
        criteria = self.get_config(key='package_filter')

        # Get success
        success = r.json()['success']
        self.config['success'] = success
        if success:
            for v in r.json()['results']:
                ct = v['voucher_code'].split("-")[0]
                if criteria not in ct:
                    continue
                # voucher_code, usage_exp, validity, price_enduser, 
                # serial, simultaneous_use,limit_dl, limit_ul, limit_tl
                vouchers.append(("%03d"%i, v['voucher_code'], v['usage_exp'], v['validity'], v['price_enduser'], v['serial'], v['simultaneous_use'], v['limit_dl'], v['limit_ul'], v['limit_tl']))
                i += 1
            # Store and save
            self.config['stored_vouchers'] = vouchers
            self.config['error_message'] = None

        # If no success, store the error message
        else:
            self.config['error_message'] = r.json()['error']['message']
        
        # Write
        self.write_configuration()

    # Read the last generated voucher from dict
    def read_last_voucher(self):
        if 'last_voucher' in self.config:
            return (self.config['last_voucher_time'], self.config['last_voucher'])
        else:
            return ("---", "---")


    def get_all_vouchers_string(self):
        entries = ['Index', 'voucher_code', 'usage_exp', 'validity', 'price_enduser', 12*' '+'serial', 'simultaneous_use', 'limit_dl', 'limit_ul', 'limit_tl']

        # Start string
        s = ""

        # Make header
        nr = []
        for entry in entries:
            s += entry + ", "
            nr.append(len(entry))
        s += "\n"

        # Make separator
        for n in nr:
            s += n*"-" + ", "
        s += "\n"

        # Fill data
        vouchers = self.read_vouchers(full=True)
        # Loop over vouchers
        for voucher in vouchers:
            # Loop over fields
            for i, field in enumerate(voucher):
                n = nr[i]
                length = n-len(str(field))
                s += length*" "
                s += str(field)
                s += ", "
            s += "\n"
        s += "\n"

        return s

    # Make a string for last voucher
    def get_generated_voucher_string(self):
        time, code = self.read_last_voucher()
        string = "-------  Hotspotsystem Voucher  -------" + "\n"
        string += "You have to activate the card before" + "\n"
        string += "first use. After activation the same" + "\n"
        string += "code can be used as the 'Username'" + "\n"
        string += "and 'Password' to log in." + "\n"
        string += "" + "\n"
        string += "Generated: %s"%time + "\n"
        string += "Code:      %s"%code + "\n"
        return string

    # Use hotspotsystem API to generate voucher
    def generate_voucher(self):
        root='https://api.hotspotsystem.com/v1.0'
        url=root+'/locations/'+self.config['LOC_ID']+'/generate/voucher.json'
        params = {'package':self.config['package']}
        r = requests.get(url, auth=(self.config['API_KEY'], 'x'), params=params)

        # Get success
        success = r.json()['success']
        self.config['success'] = success
        if success:
            # Get the time
            cur_time = strftime("%Y-%m-%d %H:%M:%S")
            # Store and save
            self.config['last_voucher'] = r.json()['access_code']
            self.config['last_voucher_time'] = cur_time
            self.config['error_message'] = None
            self.write_configuration()

        # If no success, store the error message
        else:
            self.config['error_message'] = r.json()['error']['message']
            self.write_configuration()

    # Write the updated configuration
    def write_configuration(self):
        with open(CONFIG_FILEPATH, 'w') as config_file:
            json.dump(self.config, config_file, indent=1)

    # Return the value of the config
    def get_config(self, key):
        return self.config[str(key)]

    # Write config
    def write_config(self, key, value):
        self.config[str(key)] = value
        self.write_configuration()


# Define the class for the pythonista UI
if ispythonista:
    class MyTableView(ui.View):
        def __init__(self):
            # Load the initial configuration
            self.c = Common()
            self.setup_configuration()

            #  Define buttons colors
            self.select_color = 'lightgrey'
            self.unselect_color = 'white'
            self.active_button = None
            self.button_height = 50

            # Set name of View
            self.name = 'Hotspotsystem Vouchers'
            self.background_color = 'white'
            #self.tv.delegate = MyTableViewDelegate()

            # Create TextView 1 and 2
            self.txtv_1 = ui.TextView()
            self.txtv_1.alignment = ui.ALIGN_CENTER
            self.txtv_1.editable = False
            self.txtv_1.font = ("AmericanTypewriter-Bold", 12)

            self.txtv_2 = ui.TextView()
            self.txtv_2.alignment = ui.ALIGN_CENTER
            self.txtv_2.editable = False
            self.txtv_2.font = ("AmericanTypewriter-Bold", 16)

            # Store text to view
            self.refresh_last_voucher()

            # Add the TextView
            self.add_subview(self.txtv_1)
            self.add_subview(self.txtv_2)

            # Define buttons and create the sub_views
            self.btn_1 = self.make_buttons('Index', True) #Name
            self.btn_2 = self.make_buttons('Code', True) #Size
            self.btn_3 = self.make_buttons('Time left', True) #Date

            # Make bottom button
            self.btn_4 = self.make_buttons('Refresh table', False)
            self.btn_5 = self.make_buttons('Generate', False)
            self.btn_6 = self.make_buttons('Settings', False)
            self.btn_7 = self.make_buttons('Print', False)

            # Create a tableview, with data
            self.tv = ui.TableView()
            self.tv.row_height = 30
            self.tv.data_source = MyTableViewDataSource(self.tv.row_height)

            # Update tableview data
            self.tv.data_source.items = sorted(self.c.read_vouchers(), key=itemgetter(0), reverse=True)

            # Do not allow selection on the TableView
            self.tv.allows_selection = False

            # Add the table
            self.add_subview(self.tv)

            # Show: http://omz-software.com/pythonista/docs/ios/ui.html#ui.View.present
            #self.present('full_screen')
            #self.present(hide_title_bar=True)
            self.present(hide_title_bar=True, animated=False)


        # Do setup of config dictionary
        def setup_configuration(self):
            if self.c.get_config(key='reset'):
                if not ispythonista:
                    logging.info('Get your API key from the hotspotsystem website')

                return_dict = dialogs.form_dialog(title='Input to hotspotsystem', fields=[
                    {'key':'API_KEY','type':'password','title':'API Key','value': ""},
                    {'key':'LOC_ID','type':'number','title':'Location id nr [Loc. ID]','value':'1'},
                    {'key':'package','type':'number','title':'Voucher package id nr','value':'1'},
                    {'key':'reset_code','type':'number','title':'Safety code for resetting app','value':'1234'},
                ], sections=None)

                API_KEY = return_dict['API_KEY']
                self.c.write_config('API_KEY', API_KEY)

                LOC_ID = return_dict['LOC_ID']
                if not LOC_ID.isdigit():
                    LOC_ID = "1"
                self.c.write_config('LOC_ID', LOC_ID)

                package = return_dict['package']
                if not package.isdigit():
                    package = "1"
                self.c.write_config('package', package)

                reset_code = return_dict['reset_code']
                self.c.write_config('reset_code', reset_code)

        def check_api_call(self):
            success = self.c.get_config(key='success')
            if success:
                console.hud_alert("", 'success', 0.5)
            else:
                console.hud_alert(self.c.get_config(key='error_message'), 'error')
            return success

        def make_buttons(self, name, top):
            button = ui.Button()
            button.name = name
            if name == "Print":
                button.title = ""
            else:
                button.title = name
                button.background_color = self.unselect_color

            # For all buttons
            button.border_color = 'blue'
            button.border_width = 1
            button.corner_radius = 3

            # Create the action for the top buttons
            if top:
                button.action = self.top_btn_action
            else:
                button.action = self.bot_btn_action

            # Create the view for the button
            self.add_subview(button)
            return button

        # Create the sorting actions for the buttons
        def top_btn_action(self, sender):
            names = [self.btn_1.name, self.btn_2.name, self.btn_3.name]
            sender_index = names.index(sender.name)
            if sender.background_color == (1.0, 1.0, 1.0, 1.0):    #thrid click on the same column doesn't work if it's no hardcoded color
                if sender.background_color == self.unselect_color:
                    sender.background_color = self.select_color
                    self.all_items = sorted(self.c.read_vouchers(), key=itemgetter(sender_index))
                else:
                    sender.background_color = self.unselect_color
                    self.all_items = sorted(self.c.read_vouchers(), key=itemgetter(sender_index), reverse=True)
            else:
                if self.active_button == None:
                    self.active_button = sender.name

                if sender.name == self.btn_1.name:
                    self.btn_1.background_color = self.select_color
                    self.all_items = sorted(self.c.read_vouchers(), key=itemgetter(sender_index))
                else:
                    self.btn_1.background_color = self.unselect_color

                if sender.name == self.btn_2.name:
                    self.btn_2.background_color = self.select_color
                    self.all_items = sorted(self.c.read_vouchers(), key=itemgetter(sender_index))
                else:
                    self.btn_2.background_color = self.unselect_color

                if sender.name == self.btn_3.name:
                    self.btn_3.background_color = self.select_color
                    self.all_items = sorted(self.c.read_vouchers(), key=itemgetter(sender_index))
                else:
                    self.btn_3.background_color = self.unselect_color


            self.tv.data_source.items = self.all_items
            self.tv.reload()
            self.active_button = sender.name

        @ui.in_background
        def bot_btn_action(self, sender):
            # Refresh
            if sender.name == self.btn_4.name:
                self.refresh_last_voucher()
                self.refresh_table()

            # Generate
            elif sender.name == self.btn_5.name:
                self.c.generate_voucher()
                if self.check_api_call():
                    self.refresh_last_voucher()
                    self.refresh_table()

            # Settings
            elif sender.name == self.btn_6.name:
                alert_result = console.alert('Settings',"change:", button1='Configuration', button2='Reset app!')
                #selected button is returned as an integer 

                # Change limit and offset
                if alert_result == 1:
                    return_dict = dialogs.form_dialog(title='Configuration', fields=[
                        {'key':'limit','type':'number','title':'Limit voucher list','value':self.c.get_config('limit')},
                        {'key':'offset','type':'number','title':'Offset in voucher list','value':self.c.get_config('offset')},
                        {'key':'package','type':'number','title':'Voucher package id nr','value':self.c.get_config('package')},
                        {'key':'package_filter','type':'text','title':'Filter vouchers by string','value':self.c.get_config('package_filter')},
                    ], sections=None)

                    limit = return_dict['limit']
                    if not limit.isdigit():
                        limit = "100"
                    self.c.write_config('limit', limit)

                    offset = return_dict['offset']
                    if not offset.isdigit():
                        offset = "0"
                    self.c.write_config('offset', offset)

                    package = return_dict['package']
                    if not package.isdigit():
                        package = "1"
                    self.c.write_config('package', package)

                    package_filter = return_dict['package_filter']
                    self.c.write_config('package_filter', package_filter)


                # Reset app
                elif alert_result == 2:
                    # Get safety code
                    reset_code = console.input_alert("Safety code","Please input safety code to reset app", "", "OK - Reset app!")

                    # If correct reset code
                    if reset_code == self.c.get_config('reset_code'):
                        if os.path.exists(CONFIG_FILEPATH):
                            os.remove(CONFIG_FILEPATH)
                        self.c.write_config('reset', True)
                        self.setup_configuration()

                    # If not correct safety code
                    else:
                        console.hud_alert(self.c.get_config(key='Wrong safety code.'), 'error')

                # Printe to screen
                self.txtv_1.text = "Settings:\nlimit=%s\noffset=%s"%(self.c.get_config('limit'), self.c.get_config('offset'))
                self.txtv_2.text = "package=%s"%(self.c.get_config('package'))

            # Print
            elif sender.name == self.btn_7.name:
                #console.hud_alert("Print", 'success')
                print_result = console.alert('Print vouchers',"Print or share to system?", button1='Print current voucher', button2='Print all vouchers', button3='Share to system')
 
                # Send current voucher to "real" printer
                if print_result == 1:
                    string = self.c.get_generated_voucher_string()
                    self.print_text(text=string)

                # Send all vouchers to "real" printer
                elif print_result == 2:
                    string = self.c.get_all_vouchers_string()
                    self.print_text(text=string, font_name='Courier', font_size=7)

                # Share to system
                elif print_result == 3:
                    share_result = console.alert('Share vouchers',"to system", button1='Current voucher', button2='All vouchers')

                    # Send current voucher to system
                    if share_result == 1:
                        string = self.c.get_generated_voucher_string()
                        dialogs.share_text(string)

                    # Send all vouchers to system
                    elif share_result == 2:
                        string = self.c.get_all_vouchers_string()
                        dialogs.share_text(string)


        # Refresh the table from the server
        def refresh_table(self):
            # Get vouchers from server.
            self.c.get_vouchers()
            if self.check_api_call():
                # Update data
                self.tv.data_source.items = sorted(self.c.read_vouchers(), key=itemgetter(0), reverse=True)
                self.tv.reload()

        def refresh_last_voucher(self):
            time, code = self.c.read_last_voucher()
            self.txtv_1.text = "Last voucher:\n%s"%time
            self.txtv_2.text = "%s"%code

        # Print directly to printer
        @on_main_thread
        def print_text(self, text="", font_name='Courier', font_size=10):
            # Helvetica
            UIPrintInteractionController = ObjCClass('UIPrintInteractionController')
            UISimpleTextPrintFormatter = ObjCClass('UISimpleTextPrintFormatter')
            controller = UIPrintInteractionController.sharedPrintController()
            formatter = UISimpleTextPrintFormatter.alloc().initWithText_(text).autorelease()
            font = ObjCClass('UIFont').fontWithName_size_(font_name, font_size)
            if font:
                formatter.setFont_(font)
            controller.setPrintFormatter_(formatter)
            controller.presentAnimated_completionHandler_(True, None)

        # Define layout of views
        def layout(self):
            self.tv.reload()
            # Top buttons
            self.btn_1.frame =(0*self.width/3, 0, self.width/3, self.button_height)
            self.btn_2.frame =(1*self.width/3, 0, self.width/3, self.button_height)
            self.btn_3.frame =(2*self.width/3, 0, self.width/3, self.button_height)
            # Bottom buttons
            self.btn_4.frame =(0*self.width/3, self.height - self.button_height*2, self.width/3, self.button_height)
            self.btn_5.frame =(1*self.width/3, self.height - self.button_height*2, self.width/3, 2*self.button_height)
            self.btn_6.frame =(0*self.width/3, self.height - self.button_height*1, self.width/3, self.button_height)
            self.btn_7.frame =(2*self.width/3, self.height - self.button_height*2, self.width/3, 2*self.button_height)
            # TableView frame
            self.tv.frame = (0, self.button_height, self.width, self.height - self.button_height*3)
            # Text field frame
            self.txtv_1.frame = (2*self.width/3, self.height - self.button_height*2, 1*self.width/3, 1*self.button_height)
            self.txtv_2.frame = (2*self.width/3, self.height - self.button_height*1, 1*self.width/3, 1*self.button_height)


# Define the class for the Table Data
class MyTableViewDataSource(object):
    def __init__(self, row_height):
        self.row_height = row_height
        self.width = None

    def tableview_number_of_rows(self, tableview, section):
        return len(tableview.data_source.items)

    def tableview_cell_for_row(self, tableview, section, row):
        self.width, height = ui.get_screen_size()
        cell = ui.TableViewCell()
        cell.bounds = (0,0,self.width,self.row_height)
        for i in range(3):
            self.make_labels(cell, tableview.data_source.items[row][i], i)
        return cell

    def make_labels(self, cell, text, pos):
        label = ui.Label()
        label.border_color = 'lightgrey'
        label.border_width = 0.5
        if pos == 2:
            #label.text = str(datetime.datetime.fromtimestamp(text))
            label.text = str(text)
        else:
            label.text = str(text)
        label.frame = (pos*self.width/3,0,self.width/3,self.row_height)
        label.alignment = ui.ALIGN_CENTER
        cell.content_view.add_subview(label)

#class MyTableViewDelegate(object):
#    def tableview_did_select(self, tableview, section, row):
#        print 'select'
#    def tableview_did_deselect(self, tableview, section, row):
#        print 'deselect'


# Define the class for python Interpreter
class Interpreter(object):
    def __init__(self):
        # Load the initial configuration
        self.c = Common()
        if update_config:
            self.c.write_config('reset', True)
        self.setup_configuration()

    # Do setup of config dictionary
    def setup_configuration(self):
        if self.c.get_config(key='reset'):
            if not ispythonista:
                logging.info('Get your API key from hotspotsystem')

            API_KEY = input('''Enter your API key:\n''').strip()
            self.c.write_config('API_KEY', API_KEY)

            LOC_ID = input('''Enter the location id nr [Loc. ID]:\n''').strip()
            if not LOC_ID.isdigit():
                LOC_ID = "1"
            self.c.write_config('LOC_ID', LOC_ID)

            package = input('''Enter the Voucher package id nr:\n''').strip()
            if not package.isdigit():
                package = "1"
            self.c.write_config('package', package)

            reset_code = input('''Enter a safety code, which is used when resetting the App:\n''').strip() or "1234"
            self.c.write_config('reset_code', reset_code)


    def check_api_call(self):
        success = self.c.get_config(key='success')
        if success:
            pass
        else:
            print("------------------------------------------")
            print("|    !!!!         ERROR         !!!!     |")
            print("|          %s        |"%self.c.get_config(key='error_message'))
            print("------------------------------------------")
        return success

        
    # Create initial menu for selection
    def menu(self):
        ans=True
        while ans:
            print("")
            print(" 1. Show available vouchers")
            print(" 2. Refresh voucher list from server ")
            print(" 3. Generate a voucher")
            print("")
            print(" 4. Print last voucher")
            print(" 5. Print all vouchers")
            print("")
            print(" 6. Change settings")
            print(" 7. Exit/Quit")

            ans=raw_input("What would you like to do? ") 
            if ans=="1": 
                print("")
                print("------------------------------------------")
                print("|                                        |")
                print("|   Available vouchers at location       |")
                print("------------------------------------------")
                self.print_vouchers()

            elif ans=="2": 
                print("")
                print("------------------------------------------")
                print("|                                        |")
                print("|   Refresh voucher list from server     |")
                print("------------------------------------------")
                self.c.get_vouchers()
                if self.check_api_call():
                    self.print_vouchers()

            elif ans=="3":
                print("")
                print("------------------------------------------")
                print("|                                        |")
                print("|   Generating a voucher                 |")
                print("------------------------------------------")
                self.c.generate_voucher()
                if self.check_api_call():
                    self.print_generated_voucher()

            elif ans=="4":
                print("")
                print("------------------------------------------")
                print("|                                        |")
                print("|   Print last voucher                   |")
                print("------------------------------------------")
                self.print_generated_voucher()

            elif ans=="5":
                print("")
                print("------------------------------------------")
                print("|                                        |")
                print("|   Print all vouchers                   |")
                print("------------------------------------------")
                self.print_all_vouchers_string()

            elif ans=="6":
                print("")
                print("------------------------------------------")
                print("|                                        |")
                print("|    Changing settings                   |")
                print("------------------------------------------")
                self.change_settings()

            elif ans=="7":
                print("\n Goodbye")
                ans=False

            elif ans !="" or ans =="":
                print("\n-Not Valid Choice - Try again-\n")
                ans=True

    # Change settings
    def change_settings(self):
        ans=True
        while ans:
            print("")
            print(" 1. Change default limit of shown vouchers")
            print(" 2. Change offset")
            print(" 3. Change voucher package id")
            print(" 4. Change voucher package string criteria")
            print("")
            print("    NOTE: This will delete the API key and location id.")
            print(" 5. Reset configuration file. ")
            print("")
            print(" 6. Exit menu")

            ans=raw_input("What would you like to do? ") 
            if ans=="1": 
                print("Current limit of shown vouchers: %s"%self.c.get_config('limit'))
                limit = input('''Enter new limit of shown vouchers:\n''').strip() or "100"
                if not limit.isdigit():
                    limit = "100"
                print("New limit of shown vouchers: %s\n"%limit)
                self.c.write_config('limit', limit)

            elif ans=="2":
                print("Current offset of shown vouchers: %s"%self.c.get_config('offset'))
                offset = input('''Enter new offset of shown vouchers:\n''').strip() or "0"
                if not offset.isdigit():
                    offset = "0"
                print("New offset of shown vouchers: %s\n"%offset)
                self.c.write_config('offset', offset)

            elif ans=="3":
                print("Current voucher package id: %s"%self.c.get_config('package'))
                package= input('''Enter new voucher package id:\n''').strip() or "1"
                if not package.isdigit():
                    package = "1"
                print("New voucher package id: %s\n"%package)
                self.c.write_config('package', package)

            elif ans=="4":
                print("Current voucher string criteria: %s"%self.c.get_config('package_filter'))
                package_filter= input('''Enter new criteria:\n''').strip() or ""
                print("New criteria: %s\n"%package_filter)
                self.c.write_config('package_filter', package_filter)

            elif ans=="5":
                print("Resetting configuration file.")
                reset_code = input('''Enter safety code to reset:\n''').strip() or ""

                # If correct reset code
                if reset_code == self.c.get_config('reset_code'):
                    if os.path.exists(CONFIG_FILEPATH):
                        os.remove(CONFIG_FILEPATH)
                    self.c.write_config('reset', True)
                    print("\nRESET!\n")
                    self.setup_configuration()

                # If not correct safety code
                else:
                    print("Wrong safety code provided. Not resetting.")

            elif ans=="6":
                ans=False

            elif ans !="":
                print("\n Not Valid Choice Try again")

    # Print all vouchers
    def print_vouchers(self):
        for code, price, time in self.c.read_vouchers():
            print("%3s %2s %s" % (code, price, time))
        print("")

    # Print server generated voucher
    def print_generated_voucher(self):
        string = self.c.get_generated_voucher_string()
        print("%s"%string)


    # Print server generated voucher
    def print_all_vouchers_string(self):
        string = self.c.get_all_vouchers_string()
        print("%s"%string)

## Add UI
if ispythonista:
    MyTableView()

else:   
    Interpreter().menu()
