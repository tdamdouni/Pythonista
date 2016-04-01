# coding: utf-8
'''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Setting 1</key>
	<string>On</string>
	<key>Setting 2</key>
	<string>On</string>
	<key>Setting 3</key>
	<string>On</string>
</dict>
</plist>
'''

import Projects

class MyProject(Projects.Project):
    def did_load(self):
        super(MyProject, self).did_load()
        self.name = 'Project'
        self.settings_file = __file__
        self.documents_file = 'site-packages/Documents.db'

if __name__ == "__main__":
    MyProject(