# Creating your blog with Pelican

_Captured: 2015-11-15 at 11:30 from [chdoig.github.io](http://chdoig.github.io/create-pelican-blog.html)_

[UPDATE] Disclaimer: I wrote this blog post in my first pelican blog, which used a different theme: "[pelican-bootstrap3-lovers"](https://github.com/chdoig/pelican-bootstrap3-lovers). The current design is new. When the article makes references to the design of "this blog", it's actually referring to the previous one, which looked like this:

![](http://chdoig.github.io/images/previous-blog-1.png)

![](http://chdoig.github.io/images/previous-blog-2.png)

Since this blog post gives general advice in starting a Pelican blog, I decided to keep it and add this disclaimer.

[ORIGINAL] Hello world! This blog is created using the static site generator [Pelican](http://docs.getpelican.com) and hosted on [Github Pages](https://help.github.com/categories/20/articles/). In this first post I'd like to walk you through the process of creating this blog and hopefully make it easy for you to start your own following the same steps. The [Pelican](http://docs.getpelican.com) project has great documentation and you should definitely start there. In the process of creating my blog I've discovered a lot of interesting resources to customize it, so I wanted to document it and share it.

I've organized the post in the following sections:

  * Deciding the platform: Why Pelican? What's a static site generator? What are the advantatges?
  * About Pelican: How to get started with Pelican?
  * Creating my layout and theme: How to create a responsive custom blog design with Twitter Bootstrap?
  * Additional features: How to add some widgets (Goodreads, Twitter)?
  * Publishing on Github Pages: How to get the blog up and running?

## Deciding platform

Once you decide to start a blog, one of the first questions that might come to your mind is: What platform should I use? There are many diferent blogging platforms out there and choosing the right platform for you will depend on some personal preferences. If you don't want anything to do with the command line and some code, then I'll recommend you to stop reading here and go for one of the following: [Wordpress](http://wordpress.com/), [Blogger](https://www.blogger.com/) or [Tumblr](https://www.tumblr.com/).

If you're not affraid of the command line, then you're left with the options above and a static-site generator.

### Static vs Dynamic

So, let's define first what dynamic vs static website means. In a dynamic website the contents of the site live in a database, and are converted into presentation-ready HTML only when a user wants to see the page. In a static website, the whole site is uploaded to the server as a folder full of HTML files (and images, CSS, etc). [ Nikola](http://getnikola.com/handbook.html#why-static) has a nice section on "Why Static?". It provides four reasons to chose a static versus a dynamic blog:

  * Security: Avoid the security issues of having software installed on your webhost.
  * Obsolescense: Don't need to worry about upgrading and maintaining server-side software.
  * Cost and performance: A dynamic site requires more CPU and memory to query the database, produce the HTML and send it to the user. A static site just needs to read the file from disk and send it to the user.
  * Lockin: Can easily move your website somewhere else because they are just static files.

I'll add to the list:

  * Exercise version control on the static web content.
  * Write blog posts using Markdown.
  * Nice syntax highlighting to share code.

If the reasons above convinced you to try out a static site generator, continue reading.

### Static Site Generators

Last time I checked the complete list of [static site generators](http://staticsitegenerators.net/) there where 218! That's a lot of static site generators! Probably the most popular one is [Octopress](http://octopress.org/), written in Ruby. Since I'm a Pythonista, I decided to look for Python based static site generators. Some popular ones are [Pelican](http://docs.getpelican.com), [Nikola](http://getnikola.com/) and [Hyde](http://ringce.com/hyde). I started playing around with Pelican and found it to be fun, easy, well documented and had a growing community providing themes and plugins, so I decided to stay with Pelican. I can't compare it to Nikola or Hyde since I haven't used them.

Although you might don't need much language knowledge to get the static site generator working, I would recommend choosing a language you are comfortable working with, since that will make installation and customizing easier. Then, playing around with those until you find one that is right for you.

If you're choice for a static site generator is Pelican, let's move on and learn how to get started!

## Pelican

The best way to get started with Pelican is reading the documentation [Pelican](http://docs.getpelican.com).

As a summary of the Pelican documentation here is how I proceed:

Install virtualenv and activate a virtual environment. (A virtual environment is an isolated Python system, so you don't mess up the systems Python installation).
    
    
        $ pip install virtualenv
        $ virtualenv ~/virtualenvs/pelican
        $ cd ~/virtualenvs/pelican
        $ . bin/activate

Install pelican and Markdown
    
    
      $ pip install pelican
      $ pip install markdown

Kickstart yor site
    
    
      $ pelican-quickstart

Pelican will ask you some questions about your blog and will generate the following files:
    
    
      yourproject/├── content
      │└──(pages)├── output
      ├── develop_server.sh
      ├── fabfile.py
      ├──Makefile├── pelicanconf.py       
      └── publishconf.py

Notes:

  * Content is the folder where you save your articles in Markdown or reST files.
  * Output is the folder that pelican generates with your site HTML, CSS and JS.
  * Makefile is an automated tool to help you generate, preview and upload your site.
  * fabfile.py is also another automated tool to help you generate, preview and upload your site (To use Fabfile.py you have to install Fabric `pip install Fabric`).
  * pelicanconf.py is the main settings file.
  * publishconf.py is the publish settings file.

To view your website in your browser at `http://localhost:8000`
    
    
      $ make devserver

And to stop
    
    
      $ ./develop_server.sh stop

Next, we're going to customize a theme, get some plugins, tune the pelicanconf.py file and create the content, articles and pages in either a Markdown or reST format. With the `make devserver` command you can easily see the changes in your browser.

## Creating a custom theme

I had a clear idea of how I wanted my blog to look like and this is the result. If you would like to get the theme for your blog, you can get the pelican-bootstrap3-lovers-theme [here](). I'm going to walk you through the changes I made and show you how you can customize it for your blog.

I've developed this theme using [Twitter-Bootstrap](http://getbootstrap.com/). It is self-defined as a sleek, intuitive, and powerful mobile first front-end framework for faster and easier web development. There are a lot of tools built for Bootstrap and it makes it easy and fast even for non-designers to get something decent up and running. There are a lot of nice resources built for Bootstrap. For a full list, visit the [Big Badass List of Twitter Boostrap Resources](http://www.bootstraphero.com/the-big-badass-list-of-twitter-bootstrap-resources).

I started out with Daan Debie's [Bootstrap 3 for Pelican](https://github.com/DandyDev/pelican-bootstrap3). He's done a great job of setting Bootstrap for Pelican and including [Bootswatch themes](http://bootswatch.com/), built by Thomas Park. He's also added some nice plugins and layout settings. Although that was a starting point, I've done enough customizations that it has evolved to become a theme on its own. The following is a list of the customizations I've made and that I'm going to discuss in detail next:

  * Create blog layout
  * Create color theme
  * Set a background image
  * Get a header image
  * Set your profile picture
  * Change fonts
  * Custom buttons
  * Custom social media icons

### Create blog layout

The first thing I did was create the page layout using [Bootply](http://bootply.com/), the Bootstrap playround, and [Jinja2](http://jinja.pocoo.org/), a template engine for Python that let's you do things like extend, block, for loop, etc. For example:
    
    
    {%extends"base.html"%}{% block body %}<ul>{%for article in articles %}<li><a href="{{ article.url }}">{{ article.title }}</a></li>{% endfor %}</ul>{% endblock %}

If you'd like to change your layout, first, get to know [Twitter-Bootstrap's](http://getbootstrap.com/) components and system grid.Play around with [Bootply](http://bootply.com) for a fast prototyping of your ideas. Then, edit your template files and use the `$ make devserver` command to see the changes.

### Create color theme

There is a great tool called [Paintstrap](http://paintstrap.com/). Given a color palette from [Adobe Kuler](https://kuler.adobe.com/create/color-wheel/) or [COLOURlovers](http://www.colourlovers.com/), you can set up colors for different Bootstrap components, preview the result and download the Bootstrap CSS file. It also has an extensive [Gallery](http://paintstrap.com/gallery/) of color themes that you can preview and download as well. Once you download the CSS file in your static folder, rename it to `bootstrap.yourthemename.css` and `bootstrap.yourthemename.min.css`. To use it as your theme, change the following variables of the pelicanconf.py file:
    
    
      THEME ="pelican-bootstrap3"
      BOOTSTRAP_THEME ="yourthemename"

### Set a background image

Another way to give your blog some personality is by adding a background. You can take a look at [Subtle Patterns](http://subtlepatterns.com/), which has a collection of over 300 patterns that you can preview and download. This blog uses a pattern called [Ticks](http://subtlepatterns.com/ticks/). To add a background in your theme you just have to save the file in your image folder inside the theme folder:
    
    
      yourproject/└── theme/└── images/└──background.png

Then add following code in your `style.yourthemename.css` file.

:::css   
body { background: url('../images/background.png'); }

### Get a header image

Find or take a picture and set it as your header image. You can also use Google Image Search, just be careful to filter by usage rights, like "labeled for reuse with modification", so you can use the image in your blog and/or modify it. If you don't have Photoshop, try out [GIMP](http://www.gimp.org/), it's an open source image manipulation program. I've used the Filters->Decor->Round Corners to get the round corners and the shadow. I've also added text and changed the color balance.

To add your header image, save the image under:
    
    
      yourproject/└── content/└── images/└──yourheaderimage.png

and add the following lines in your `pelicanconf.py` file:
    
    
    STATIC_PATHS =['images']
    HEADER_IMAGE ="yourheaderimage.png"

### Set your profile picture

To set your profile picture, save your profile image under the same folder as the header image:
    
    
      yourproject/└── content/└── images/└──yourprofilepicture.png

and add the following line to your `pelicanconf.py` file:
    
    
    STATIC_PATHS =['images']
    PROFILE_PICTURE ="yourprofilepicture.png"

### Change fonts

You can use [Google Fonts](http://www.google.com/fonts/) to find a pair of fonts that you like. For some inspiration on font combination read [this article](http://designshack.net/articles/css/10-great-google-font-combinations-you-can-copy/). The two recomendations that I've followed from this article were: Go easy and Contrast is key. I've picked Dancing Script for the headers and Cabin for the body. Once you find your fonts, copy the url that [Google Fonts](http://www.google.com/fonts/) provides you and set the font you want each of the elements to have in your `style.yourthemename.css`. For example:
    
    
    @import url(http://fonts.googleapis.com/css?family=yourfontname1);@import url(http://fonts.googleapis.com/css?family=yourfontname2);
    h1,h2,h3,h4,h5,h6,.h1,.h2,.h3,.h4,.h5,.h6{font-family:'yourfontname1;}
    p{font-family:'yourfontname2';}

### Custom buttons

Design a custom button using Charlie Park's [Beautiful Buttons for Twitter Bootstrappers](http://charliepark.org/bootstrap_buttons/). Copy the CSS to `your style.yourtheme.css` file and change `.btn-custom` to `.btn-default`. So you should have something like:
    
    
    .btn-default{# YOUR CSS CODE}

### Custom social media icons

Check out [Deviantart](http://www.deviantart.com/?qh=&section=&global=1&q=social+media+icons) for free social media icons. There are a lot of great designs. If you can't find any that you like you can always make them yourself or modify them using [GIMP](http://www.gimp.org/). Save the icons you would like to use under the following folder:
    
    
      yourproject/└── theme/└── images/└──socialmediasite-icon.png

Make sure you use the following notation: `socialmediasite-icon.png`, e.g. twitter-icon.png or github-icon.png.

### Syntax higlighting

Pelican uses by default Pygments for highlighting. I wasn't happy with how Pygments parses words inside the `<code>` tag, so I looked for an alternative. I found [Prism](http://prismjs.com/), it's easy to use, has already some beautiful syntax highlighting color schemes and uses a more elegant HTML syntax, just uses `<code>` tags, along with the recommended way to define a code language in HTML 5, a language-xxxx class. You can preview different available color schemes and download the one you'd like to use for your blog at [Prism](http://prismjs.com/). To use Prism I have deactivated Pygments and added the `prism.css` file and `prism.js` to `base.html`:
    
    
    <!--link href="{{ SITEURL }}/theme/css/pygments.css" rel="stylesheet"--><linkhref="{{ SITEURL }}/theme/css/prism.css"rel="stylesheet"/><scriptsrc="{{ SITEURL }}/theme/js/prism.js"></script>

When using Markdown you'll need to write your code like this with the aproppriate `language-XXXX`:
    
    
    ~~~~{.language-markup}<!--link href="{{ SITEURL }}/theme/css/pygments.css" rel="stylesheet"--><link href="{{ SITEURL }}/theme/css/prism.css" rel="stylesheet"/><script src="{{ SITEURL }}/theme/js/prism.js"></script>~~~~

And setup your `pelicanconf.py` file to:
    
    
    MD_EXTENSIONS =['extra']

If you'd rahter keep using Pygments in your blog, just set it up in `base.html` to:
    
    
    <linkhref="{{ SITEURL }}/theme/css/pygments.css"rel="stylesheet"><!--link href="{{ SITEURL }}/theme/css/prism.css" rel="stylesheet" /--><!--script src="{{ SITEURL }}/theme/js/prism.js"></script-->

And leave the MD_EXTENSIONS to:
    
    
    MD_EXTENSIONS =['codehilite(css_class=highlight)']

## Additional features

I have also added two widgets to my blog: Latest Tweets and Goodread quotes. To activate them you'll need to set up the following variables in your `pelicanconf.py` file:
    
    
    TWITTER_USERNAME = XXXXX
    TWITTER_WIDGET_ID = XXXXX
    GOODREADS_ID = XXXXX

To get a `TWITTER_WIDGET_ID`, go to: `https://twitter.com/settings/widgets` and `Create new`. You'll find the `TWITTER_WIDGET_ID` under the html or in the site url:

`https://twitter.com/settings/widgets/TWITTER_WIDGET_ID/edit`

To get your `GOODREADS_ID` go to your Goodreads profile. The url will be:

`https://www.goodreads.com/user/show/GOODREADS_ID`

Copy this id into the `pelicanconf.py`. This widget will display a random quote from your quotes list.

## Publishing to Github

For information regarding publishing your blog on Github check [Pelican](http://pelican.readthedocs.org/en/3.3.0/tips.html#publishing-to-github) or [Github](https://help.github.com/articles/user-organization-and-project-pages).

I'm using a User Page, so I just have to set up a repo named `chdoig.github.io`, and upload my the output folder there.

And we're done! Hopefully now you'll be able to set up your blog and customize it to your own preferences. If you have any questions, I'll be happy to help you out! Thank you for reading!

## Final notes

The [Pelican](http://docs.getpelican.com/en/3.5.0/index.html) version used for this article was: v.3.3 and the "pelican-bootstrap3-lovers" theme can be found [here](https://github.com/chdoig/pelican-bootstrap3-lovers).
