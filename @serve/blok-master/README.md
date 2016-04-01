# blok
A simple static site generator for Pythonista + Editorial on iPad & iPhone: write in Editorial and send to blok.

If you have feedback or actually use this, please let me know! Pull requests welcome.

**How it works**

1. In `build_site()`, each post is read, converted to html, and then added to an html template and written to the output directory.

    If in `posts/` there's a post `03-05-2015-test-post.markdown`, it will be wriiten to `OUTPUT_DIR/test-post/index.html`.

2. After the posts are written, a link is added for each post in the main index.html. For the test post above, the link would be `/test-post/`. This gives nice links with no '.html' on the end.

3. Next, any CSS files in `STATIC_DIR/css` are copied to `OUTPUT_DIR/css`. Links to css files are added in the pervious step.

    The css-copying code will probably get made into a function and generalized, so we can copy images and so on.

**Editorial workflows**:
* [New post](http://www.editorial-workflows.com/workflow/5812790350577664/oa40mJqmRxY) - a UI for making a new post in Editorial. If you tell it to use the existing file, the contents of the file are added to the post metadata, like so:
```
title: Example title
date: 16-04-2015
slug: example-title
====
(existing file contents here)
```

* [Post -> Blok](http://www.editorial-workflows.com/workflow/5900215483629568/b1X0ckOwSCY) - sends the current post to Blok, where it is added to the posts folder as a markdown file. Then, when the site is built, the post will be included.

**Todo**
- There is currently no built in mechanism for deployment. Since my iPad is jailbroken, I just made a symlink in `/var/private/mobile` to Pythonista's documents folder, and then from there I can copy things out. Maybe '[githubista](https://github.com/mmurdoch/githubista)' is a possibility for github pages?
