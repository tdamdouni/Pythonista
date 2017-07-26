# https://forum.omz-software.com/topic/4034/simple-ui-to-run-script2-args/21
# in script2.py, select one of the following and rename it to main()

def default_arg_main(script_name, first_name, middle_name, last_name=''):
    last_name = last_name or 'Bonehead'
    fmt = "{}: Your full name is {} {} {}."
    print(fmt.format(script_name, first_name, middle_name, last_name))

def if_main(*args):
    if len(args) == 4:
        fmt = "{}: Your full name is {} {} {}."
    else:
        fmt = "{}: Your full name is {} {}."
    print(fmt.format(*args))

def join_main(*args):
    print("{}: Your full name is {}.".format(args[0], ' '.join(args[1:])))

def list_main(*args):
    fmt = ('Zero sys.argv is not possible!',
           'Usage: {} first_name, [middle_name, [last_name]]',
           "{}: Your full name is {}.",
           "{}: Your full name is {} {}.",
           "{}: Your full name is {} {} {}.")[len(args)]
    print(fmt.format(*args))

# and then...
print('=' * 44)
main(*sys.argv)