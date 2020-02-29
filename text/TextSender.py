from __future__ import print_function
import ui

def fieldEdited(sender):
    t=sender.text   # note change
    print(t)

view = ui.View()
view.background_color = 'white'


for loop in range(1,11):
    #print loop
    fieldName ='field' + str(loop)                     
    field = ui.TextField()
    field.name = fieldName
    field.text= 'type something'
    field.center = (70,(90+loop*30)) 
    field.height=27
    field.width=82
    field.action = fieldEdited                      
    view.add_subview(field)                          

view.present(style='full_screen',hide_title_bar='True')
