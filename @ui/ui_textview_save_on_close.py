import ui
 
filename = 'name.txt'
 
class GetUsernameView(ui.View):
    def __init__(self, username=None):
        self.name = self.__class__.__name__
        textfield = ui.TextView(name='namefield')
        textfield.height = 25
        textfield.text = self.username = username or self.read_username()
        self.add_subview(textfield)

        self.hidden = True
        self.present('sheet')
        # somtimes it is good to be self-centered
        textfield.center = self.center
        self.hidden = False
        
    @classmethod
    def read_username(cls, filename=filename):
        username = None
        try:
            with open(filename) as in_file:
                for line in in_file.readlines():
                    username = line.strip() or username
        except IOError:
            pass
        return username or 'Player 1'

    def will_close(self):
        self.username = self['namefield'].text.strip() or self.username
        if self.username:
            with open(filename, 'w') as out_file:  
                out_file.write(self.username)
    
root_view = GetUsernameView()
ui.in_background(root_view.wait_modal())
print(root_view.username)
