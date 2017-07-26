# https://gist.github.com/TutorialDoctor/6c0c1fe3ca65c5981d86

# WIP
# By the Tutorial Doctor
# CLASSES
#------------------------------------------------------------
class Element:
    count = 0
    def __init__(self):
        self.tag = 'p'
        self.id = "elementID"
        self.html = "<%s id=\"%s\"></%s>"%(self.id,self.tag,self.tag)
        self.innerHtml = ''
        Element.count+=1
    
    def appendTo(self,FILE="index.html"):
        """Appends the element to a file args(File) return(None)"""
        with open(FILE,'a') as outfile:
            outfile.write('\n'+str(self))
    
    def __str__(self):
        return self.html
#------------------------------------------------------------
class Video(Element):
    count = 0
    
    def __init__(self,src):
        Element.__init__(self)
        self.tag = 'video'
        self.src = src
        self.width = 800
        self.height =600
        self.autoplay = 600
        self.loop = False
        self.properties = 'autoplay' #I need to be able to change this outside of the class
        self.html = "<%s id = \"%s\" src =\"%s\" %s></%s>"%(self.tag,self.id,self.src,self.properties,self.tag)
        print('video created')
        Video.count+=1
#------------------------------------------------------------


# IMPLEMENTATION
#------------------------------------------------------------
video1 = Video("Jurassic World.mp4")
video1.appendTo("index.html")
#------------------------------------------------------------


# CUSTOM FUNCTIONS
#------------------------------------------------------------
def addCount(element,FILE,times=1):
    """Adds an element to a file a number of times args(element,file,integer) return(None)"""
    for i in range(0,times):
        element.appendTo(FILE)


