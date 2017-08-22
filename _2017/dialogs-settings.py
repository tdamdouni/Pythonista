# https://forum.omz-software.com/topic/4113/how-do-i-or-how-can-i-add-a-separator-line-in-the-ui-editor

from dialogs import *

dead={'type':'switch','title':'dead'}
resting={'type':'switch','title':'resting'}
stunned={'type':'switch','title':'just stunned'}
section1=('Parrot',[dead, resting, stunned] )

spam={'type':'switch','title':'spam'}
spamity={'type':'switch','title':'spam'}
spaM={'type':'switch','title':'spam'}
section2=('Spam',[spam, spamity, spaM],'SpammitySpam' )


f = form_dialog(title='Python Settings', sections=
    [section1, section2])

