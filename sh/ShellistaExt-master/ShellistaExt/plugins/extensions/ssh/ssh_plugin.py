'''ssh:
Usage: 
    addhost save_name hostname user [password]
    listhost
    delhost name
    connect save_name
    connect hostname user password
'''
from ssh import SSH

alias = []

def main(self, line):
    args = line.split()
    ssh = SSH()
    if len(args) == 0:
        print '''Usage: 
    addhost save_name hostname user [password]
    connect save_name
    connect hostname user password
    '''
        return
    if args[0] == 'addhost':
        ssh.addhost(' '.join(args[1:]))
    elif args[0] == 'connect':
        ssh.connect(' '.join(args[1:]))
    elif args[0] == 'listhost':
        ssh.listhost()
    elif args[0] == 'delhost':
        ssh.delhost(' '.join(args[1:]))
    else:
        print __file__.__doc__
        return
        
if __name__ == '__main__':
    main('connect rdr')
    
