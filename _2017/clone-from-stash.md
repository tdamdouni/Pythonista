[~/Documents]$ gh create_key newipadkey
Creating a ssh key in ~/.ssh/
ssh-keygen -d rsa -b2048
ssh keys generated with rsa encryption

[~/Documents]$ git clone ssh://git@github.com/jsbain/stash.git stash

~/.ssh/known_hosts

github.com ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ==

print full traceback

stashconf py_traceback 1

automatically start interactive pdb when exceptions occur

stashconf py_pdb 1

For paramiko issues, you could, in the 2.7 interpreter in the console, type

import paramiko
paramiko.util.log_to_file('paramikolog.txt')
