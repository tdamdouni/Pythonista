# coding: utf-8

# https://forum.omz-software.com/topic/1584/pandoc-flavoured-markdown-preview/3

def whack_the_yaml(text):
	if not text.strip():
		return text
	start_index = end_index = -1  # impossible indexes
	lines = text.splitlines()
	for i, line in enumerate(lines):
		if start_index == -1:
			if line.strip() == '---':
				start_index = i
		else:
			if line.strip() in ('...', '---'):
				end_index = i+1
				break
	if start_index == -1 or end_index == -1:
		console.hud_alert('No yaml block was found.', 'error')
		return text
	else:
		console.hud_alert('Removing {} lines of yaml.'.format(end_index-start_index))
		return '\n'.join(lines[:start_index] + lines[end_index:])

