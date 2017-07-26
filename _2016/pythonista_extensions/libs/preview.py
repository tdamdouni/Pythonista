# coding: utf-8

# https://gitlab.com/atronah/pythonista_extensions/tree/master

import os
import ui
from libs.misc import get_sources, get_source_content
from markdown2 import markdown, markdown_path


def preview_html(source, title = 'HTML Preview'):
    webview = ui.WebView(title)
    webview.load_html(source)
    webview.present()
    

def preview_markdown(source, is_path = False, title='Markdown Preview'):
    TEMPLATE = '''
        <!doctype html>
        <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width">
                <title>Preview</title>
                <style type="text/css">
                    body {
                        font-family: helvetica;
                        font-size: 15px;
                        margin: 10px;
                    }
                </style>
            </head>
            <body>{{CONTENT}}</body>
        </html>
    '''
    extras = ['fenced-code-blocks', 
              'cuddled-lists',
              'header-ids']
            
    if not source:
        print('No input text found. Use this script from the share sheet in an app like Notes.')
        return
    converter = markdown_path if is_path else markdown
    converted = converter(source, extras=extras)
    html = TEMPLATE.replace('{{CONTENT}}', converted)
    preview_html(html, title)


def process_sources(content_type='html'):
    content_type_map = {'html': preview_html,
                        'md': preview_markdown} 
    
    assert content_type in content_type_map 
    
    for source, type in get_sources():
        content = get_source_content(source, type)
        if content:
            content_type_map[content_type](content.decode('utf8'))
            return True

    return False
            
