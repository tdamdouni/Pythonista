# Python: Flask – Generating a Static HTML Page

_Captured: 2017-05-01 at 20:48 from [dzone.com](https://dzone.com/articles/python-flask-generating-a-static-html-page?edition=293882&utm_source=Daily%20Digest&utm_medium=email&utm_campaign=dd%202017-05-01)_

Discover [how to focus on operators for Reactive Programming](https://dzone.com/go?i=190137&u=https%3A%2F%2Fblog.wakanda.io%2Freactive-programming-operators%2F%3Futm_source%3Ddzone%26utm_campaign%3Dblog-article%26utm_medium%3Dreferral) and how they are essential to react to data in your application. Brought to you in partnership with [Wakanda](https://dzone.com/go?i=190137&u=https%3A%2F%2Fwww.wakanda.io%2F).

Whenever I need to quickly spin up a web application, Python's [Flask](http://flask.pocoo.org/) library is my go to tool. Recently, however, I found myself wanting to generate a static HTML page to upload to S3 and wondered if I could use it for that as well.

It's actually not too tricky. If we're in [the scope of the app context](http://stackoverflow.com/questions/31830663/how-to-render-template-in-flask-without-using-request-context) then we have access to the template rendering that we'd normally use when serving the response to a web request.

The following code will generate an HTML file based on a template file templates/blog.html:

templates/index.html

If we execute the Python script it will generate the following HTML:

And we can finish off by redirecting that output into a file:

We could also write to the file from Python, but this seems just as easy!

[Learn how divergent branches can appear in your repository](https://dzone.com/go?i=190138&u=https%3A%2F%2Fblog.wakanda.io%2Fanimated-git-4-understand-divergent-branches-appear-fetching-remote-repository%2F%3Futm_source%3Ddzone%26utm_campaign%3Dblog-article%26utm_medium%3Dreferral) and how to better understand why they are called "branches". Brought to you in partnership with [Wakanda](https://dzone.com/go?i=190138&u=https%3A%2F%2Fwww.wakanda.io%2F).
