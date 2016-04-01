# coding: utf-8
'''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Setting 1</key>
	<string>Value 1</string>
	<key>Setting 2</key>
	<string>vALUE 2</string>
	<key>Setting 3</key>
	<string>Value 3</string>
</dict>
</plist>
'''

import os, plistlib, editor, ForumCodeBlock

class Settings (object):
    def __init__(self):
        self.__make_self()

    def __make_self(self):
        self.Settings_version = '4.0'
        self.Settings_source_code = 'Original by @tony.'
        self.Settings_permissions = 'Permission to use/subclass/redistribute, but NOT to modify code.'
        self.settings_file = None
        self.settings_dict = None
        self.__iR = 0

    def open_settings(self):
        if self.settings_file[:7] == 'http://':
            fcb = ForumCodeBlock.ForumCodeBlock()
            fcb.forum_url = self.settings_file
            fcb.block_type = 'plist'
            self.settings_dict = plistlib.readPlistFromString(fcb.text())
        else:
            with open(self.settings_file, 'r') as fS: self.__sA = fS.read()
            self.__iS = self.__sA.find('<?xml')
            self.__iF = self.__sA.find('</plist>') + 8
            self.settings_dict = plistlib.readPlistFromString(self.__sA[self.__iS:self.__iF])
        return True

    def get_setting(self, sK):
        while self.__iR != 0: pass
        return {'setting': sK , 'value': self.settings_dict[sK]}

    def set_setting(self, sK, sV):
        self.__iR += 1
        self.settings_dict[sK] = sV
        self.__iR -= 1
        return True

    def close_settings(self):
        while self.__iR != 0: pass
        if self.settings_file[:7] == 'http://':
            pass
        else:
            sPl = plistlib.writePlistToString(self.settings_dict)
            sN = self.__sA[0:self.__iS] + sPl[:-1] + self.__sA[self.__iF:]
            with open(self.settings_file, 'w') as fS: fS.write(sN)
            if editor.get_path() == self.settings_file:
                tS = editor.get_selection()
                iD = 0 if tS[0] <= self.__iF else len(sN) - len(self.__sA)
                editor.replace_text(0, len(editor.get_text()), sN[:-1])
                editor.set_selection(tS[0] + iD, tS[1] + iD)
            return True
        self.settings_dict = None

if __name__ == "__main__":
    if True:
        s = Settings()
        s.settings_file = __file__
        s.open_settings()
        s.set_setting('Setting 2', s.get_setting('Setting 2')['value'].swapcase())
        s.close_settings()
    else:
        s = Settings()
        s.settings_file = 'http://omz-forums.appspot.com/pythonista/post/5832111260958720'
        s.open_settings()
        for key in s.settings_dict:
            print key + '\n\t' + s.settings_dict[key]
        s.close_settings(