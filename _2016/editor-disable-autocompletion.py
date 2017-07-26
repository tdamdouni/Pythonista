# https://forum.omz-software.com/topic/3692/auto-fill-correct-blowing-up-editor-app/6

import editor
editor._get_editor_tab().editorView().completionProvider=None

# disable jedi

editor._get_editor_tab().editorView().completionProvider().fallbackCompletionProvider=None
