# coding: utf-8
from __future__ import print_function
import urllib2, bs4

class ForumCodeBlock(object):
    def __init__(self):
        self.__make_self()

    def __make_self(self):
        self.ForumCodeBlock_version = '3.1'
        self.ForumCodeBlock_source_code = 'Original by @tony.'
        self.ForumCodeBlock_permissions = 'Permission to use/subclass/redistribute, but NOT to modify code.'
        self.forum_url = None
        self.block_type = None

    def text(self):
        for fcb in bs4.BeautifulSoup(urllib2.urlopen(self.forum_url).read()).find_all('code'):
            sT = fcb.getText()
            if self.block_type == 'python':
                if sT[:3] == "'''" or sT[:6] == 'import':
                    return sT
            elif self.block_type == 'plist':
                if sT[:5] == '<?xml':
                    return sT
        return None

if __name__ == "__main__":
    fcb = ForumCodeBlock()
    fcb.forum_url = 'http://omz-forums.appspot.com/pythonista/post/5885488242098176'
    fcb.block_type = 'python'
    print(fcb.text())
    fcb.block_type = 'plist'
    print(fcb.text())