from __future__ import print_function
# https://forum.omz-software.com/topic/681/get-workflow-name-programmatically

import editor
import os
import json

with open(os.path.join(editor.get_workflows_path(), 'Commands.edcmd')) as f:
	wf_infos = json.load(f)
	for wf in wf_infos:
		print(wf['filename'] + ' -- ' + wf['title'])
# --------------------

import json
workflow_filename = 'someworkflow.wkflw' # change this

# Read the workflow data:
with open(workflow_filename, 'r') as f:
	workflow_dict = json.load(f)
	
# Modify it:
actions = workflow_dict['actions']
first_action = actions[0]
first_action['customTitle'] = 'Foo Bar'

# Save the modified workflow data:
with open(workflow_filename, 'w') as f:
	json.dump(workflow_dict)

