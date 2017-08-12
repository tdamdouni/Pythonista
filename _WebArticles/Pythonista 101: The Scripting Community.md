# Pythonista 101: The Scripting Community

_Captured: 2015-09-29 at 00:09 from [ipad.appstorm.net](http://ipad.appstorm.net/how-to/utilities/pythonista-101-the-scripting-community/)_

A real asset to Pythonista is the enthusiastic developer community that's sprung up around the app. The [Pythonista Forums](http://omz-software.com/pythonista/forums/) are a rich source of support when struggling to debug a script of your own, or when looking to release a script for use by the rest of the Pythonista community.

As it has become a common place to post Pythonista scripts, we'll be showing off a few select examples found in the Pythonista forums to help give you an idea of the sort of thing Pythonista is capable of. We'll also explain how to integrate a script from the web into your copy of Pythonista.

_Like this article? Stay up to date with the latest changes by subscribing to our [RSS feed](http://feeds2.feedburner.com/ipadappstorm) or by following us either on [Twitter](https://twitter.com/ipadappstorm), [Facebook](http://facebook.com/ipadappstorm), [Google+](https://plus.google.com/100501393336992877365/posts) or [App.net](https://alpha.app.net/ipadappstorm)._

## Script Showcase

### Basic Calculator

[https://gist.github.com/SebastianJarsve/5382778](https://gist.github.com/b0644f5ed1d94bd32805)

While this may not seem like the most exciting thing to do with Pythonista, the code behind this simple script is quite elegant, and there's a lot to be learned from studying it. Those new to Python, or coding in general should be taking notes.

### File Browser

<https://gist.github.com/omz/4051823>

A favorite of mine, this exceptionally simple script lets you browse through that thing Apple always says iOS devices don't have: a file system. Turns out they _do_ have one. And this is how you can check it out. It's more a "look-but-don't touch" approach, but still fun to play with, and the fact that it's only 10 lines of code is amazing.

### Space Shooter Game

<https://gist.github.com/anonymous/40a696fcacf1b4e3c13f>

Yup, you can use Python to write games too. And here's a nice one. While the physics may not blow anyone away with their realism, it's a fun game, and gives those interested in game design a place to start from.

### Top Apps

<https://gist.github.com/omz/4034379>

This one too may not seem all that impressive, but it's the code that shines through here, not necessarily the simple thing it produces. This script introduces the RSS Feed Parsing module, something we'll be looking at more later.

### PIL Meme Generator

<https://gist.github.com/omz/4034426>

The Python Image Library is an incredibly powerful tool, and this little script really only scratches the surface of it. We'll be looking at the PIL in more depth later, but for now, play around with this script and whatever cat pictures you have laying around.

### Advanced Shell Commands

<https://gist.github.com/pudquick/4139094>

This one is definitely a bit out of your average users comfort zone, but then again, Pythonista itself isn't really for the mainstream consumer. This script gives basic command line access to the Pythonista directory, letting you manipulate your scripts with [bash-like](http://en.wikipedia.org/wiki/Bash_\(Unix_shell)) commands.

### Breakout Clone

<https://gist.github.com/SebastianJarsve/5305895>

Another game, this Breakout Clone also has some rough physics simulation, but is a great example of the kind of games simple Python scripts are capable of. We might be revisiting this one later as well.

## Script Integration

Now that we've seen some of the cool scripts available for Pythonista, the question remains: how do we integrate these into our personal copies of Pythonista?

The first, rather simple way, is to copy the code off of a site and into a new Python script. There is a slicker way though, which allows us to leverage Pythonista itself to load new scripts into it. The creator of Pythonista, Ole Zorn, has built a python script that takes Github Gist URLs, downloads the file, and adds the new script to your library. To top it all off, Pythonista lets you add any script in your library to the app's Actions Menu, giving you quick, one tap access to this feature.

First, open up this Github Gist on your iPad: <https://gist.github.com/b0644f5ed1d94bd32805>

![130523-The-Scripting-Community1](http://cdn.appstorm.net/ipad.appstorm.net/authors/zachlebar2/130523-The-Scripting-Community1.jpg)

Once open, select all the text in the script and copy it to your clipboard.

![130523-The-Scripting-Community2](http://cdn.appstorm.net/ipad.appstorm.net/authors/zachlebar2/130523-The-Scripting-Community2.jpg)

> _Now jump into Pythonista, and create a new blank project._

![130523-The-Scripting-Community3](http://cdn.appstorm.net/ipad.appstorm.net/authors/zachlebar2/130523-The-Scripting-Community3.jpg)

Now paste the script into the new project, and rename it to something you'll remember like "New from Gist".

![130523-The-Scripting-Community4](http://cdn.appstorm.net/ipad.appstorm.net/authors/zachlebar2/130523-The-Scripting-Community4.jpg)

Now the fun part comes in. Tap on the Settings icon, and then tap on Actions Menu section.

![130523-The-Scripting-Community5](http://cdn.appstorm.net/ipad.appstorm.net/authors/zachlebar2/130523-The-Scripting-Community5.jpg)

Scroll down to the bottom of the Actions Menu section. Here you'll find a listing of all the scripts in your Pythonista Library. By tapping on one or more of them you'll add a button to the Actions Menu which will run the script when you tap that button.

![130523-The-Scripting-Community6](http://cdn.appstorm.net/ipad.appstorm.net/authors/zachlebar2/130523-The-Scripting-Community6.jpg)

And now we see the "New from Gist" button appear in the Actions Menu. Go ahead and try it with any of the Gists mentioned earlier in this article.

![130523-The-Scripting-Community7](http://cdn.appstorm.net/ipad.appstorm.net/authors/zachlebar2/130523-The-Scripting-Community7.jpg)

## Next Week

Ok, so now that you're a little more familiar with operating Pythonista, and have seen what the app is capable of, as well the strong community behind it, you're ready to get your hands dirty with writing some Python code.

That's what we tackle next week. Python wrangling.
