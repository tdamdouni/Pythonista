# https://gist.github.com/jsbain/4e1f068c5bbc723bf2ef

import notification, uuid, sys

def reminder(message, delay=3600*24, uid=None, 
             sound_name='default', 
             action=None, action_args=(), 
             interval=3600, 
             num_reminders=5):
    ''' call a script after a delay, and keep reminding until the notification is acknowledged.
    uses a uid to access all instances of this reminder, for deleting or finding when the next instance is scheduled.
    
    adding a new reminder with the same uid wipes out existing reminders with that uid.
    
    parameters:
    
    message  string message
    delay    seconds
    uid      string, or None to use random uuid
    sound_name string name of a sound, or '' for no sound
    action    string name of a script
    action_args tuple of args to pass to action.  should be escaped if needed
    interval  time in seconds between reminders
    num_reminders number of reminders to issue
    
    '''
    
    if uid is None:
        #create random uid
        uid=uuid.uuid4()
        
    #delete any existing reminders with this uid
    delete_reminder(uid)
    
    for i in range(num_reminders):
        url='pythonista://reminder?action=run&argv={}&argv={}'.format(uid,action)
        argstr=''
        for a in action_args:
            argstr+='&argv={}'.format(a)
        notification.schedule(message, delay+i*interval, sound_name, url+argstr)
        
def delete_reminder(uid):
    ns=notification.get_scheduled()
    for n in ns:
        args=n['action_url'].split('&argv=')
        if args[0].startswith('pythonista://reminder?'):
            if args[1]==uid:
                notification.cancel(n)
                
def next_reminder(uid):
    ns=notification.get_scheduled()
    t=0
    for n in ns:
        args=n['action_url'].split('&argv=')
        if args[0].startswith('pythonista://reminder?'):
            if args[1]==uid:
                t=n['fire_date']
                return t
    return float('inf')
    
def get_uids():
    '''returns dict of uids containing the soonest notification.  get_uids().keys() returns valid keys'''
    ns=notification.get_scheduled()
    uids=dict()
    for n in reversed(ns):
        args=n['action_url'].split('&argv=')
        if args[0].startswith('pythonista://reminder?'):
            uids[args[1]]=n
    return uids
    
if __name__=='__main__':
    import webbrowser
    # callback called from notification
    # to keep this simple, the callbacks will be of form
    # 'pythonista://reminder?action=run&argv=uuid&argv=scriptname&argv=arg0&...')  
    # uid is a unique id used to identify the original action
    try:
        uid=sys.argv[1]
        scriptname=sys.argv[2]
    except IndexError:
        print('not enough args')
        raise
        
    delete_reminder(uid)
    
    argstr=''
    otherargs=sys.argv[3:]
    for a in otherargs:
        argstr+='&argv={}'.format(a)
        
    webbrowser.open('pythonista://{}?action=run'+argstr)
    
            argstr=''
        for a in action_args:
            argstr+='&argv={}'.format(a)
# Could be rewritten as...
        argstr=''.join(['&argv={}'.format(a) for a in action_args])

#####

        if args[0].startswith('pythonista://reminder?'):
            if args[1]==uid:
# Could be rewritten as...
        if args[0].startswith('pythonista://reminder?') and args[1]==uid: