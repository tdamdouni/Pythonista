
#ShellistaExt

##Create a Plugin

To create a plugin follow this simple example. The name of the .py is the main name of the command followed by _plugin.py. All plugins should be placed inside of the plugin directory.

*sample_plugin.py*

    '''This is the help info for the plugin'''
    
    #bash breaks up the return string into a list
    #pprint is used for better printing of directories
    #This is a relative import. Neither tools are needed. 
    #You can parse the string passed into main any way you like
    from .. tools.toolbox import bash,pprint
    
    #List all aliases for the pluing, if any.
    alias = ['samp'] 
    
    #This is the entry point into the plugin
    def main(line): 
      #This breaks the input up into a list of commands
      args = bash(line) 
      
      #main code here
    

