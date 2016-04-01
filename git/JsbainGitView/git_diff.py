class source(object):
    PATH=0
    INDEX=1
    PREV=2
    

from difflib import HtmlDiff
import os

import ui

def diff_working(repo,file,src=source.PATH):
    store=repo.object_store
    index=repo.open_index()
    
    tree=store[store[repo.head()].tree]
    parent_tree=store[store[store[repo.head()].parents[0]].tree]
    
    tree_ver=store[tree.lookup_path(store.peel_sha,file)[1]].data


    local_ver=open(os.path.join(repo.path,file)).read()
    h=HtmlDiff(wrapcolumn=70,tabsize=4)
    if src==source.PATH:
        f=h.make_file(tree_ver.splitlines(),local_ver.splitlines(), file, 'last commit:'+repo.head())
    elif src==source.INDEX:
        index_ver=store[index._byname[file].sha].data
        f=h.make_file(tree_ver.splitlines(),index_ver.splitlines(),file+' staged change', 'last commit'+repo.head())
    else:
        parent_tree_ver=store[parent_tree.lookup_path(store.peel_sha,file)[1]].data
        f=h.make_file(parent_tree_ver.splitlines(),tree_ver.splitlines(), file+' HEAD','HEAD^1')        
    return f

#f=diff_working(porcelain.open_repo('.'),'gitui.py')
#w=ui.WebView()
#w.load_html(f)
#w.present()
