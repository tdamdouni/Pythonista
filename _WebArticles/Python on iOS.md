# Python on iOS

_Captured: 2016-12-21 at 15:49 from [lukasa.co.uk](https://lukasa.co.uk/2016/12/Python_on_iOS/)_

![Python on iOS](https://lukasa.co.uk/images/palais.jpg)

This holiday I discovered [Pythonista](https://itunes.apple.com/gb/app/pythonista-3/id1085978097?mt=8), and my mind was blown.

In the iOS world, Pythonista is a well known quantity. I can find articles about it from sources like MacStories from back in [2012](https://www.macstories.net/stories/automating-ios-how-pythonista-changed-my-workflow/). Back then it was fairly rudimentary: no support for folders, no ability to import code from outside the app (at least not easily), and limited ability to interact with lots of parts of the OS. But it was clearly useful to a lot of people as a powerful tool for automating their iOS devices.

However, it seems like many of the people who were using this to automate their iOS devices weren't Python developers, and most Python developers didn't seem to be fully aware that it existed. If they were, they would have found that 2012's little Python interpreter in an iOS app has turned into a nearly fully-fledged Python programming environment. How did this happen? In no small part, it's down to [Stash](https://github.com/ywangd/stash).

Stash is a pure-Python implementation of a Bash-like shell for Pythonista. Essentially, you download and install it and then execute a helper script inside Pythonista. That helper script opens up a new console window and gives you, amazingly, a shell prompt with a _filesystem_:

![A view of the Pythonista shell](https://lukasa.co.uk/images/pythonista/shell.png)

This is a little bit mind blowing. But it gets better because, you see, this shell has got some game. It comes with a few killer applications essentially reimplemented using Python, the most notable of which are `git` and `pip`. Now, to be clear, these applications are very much _reimplementations_ of the standard tools: they often don't have the same syntax as the originals and they have weird limitations that the others don't have. But together they let you do this:

![Installing and cloning with pip and git](https://lukasa.co.uk/images/pythonista/git_pip.png)

That's me installing a Python package from PyPI and cloning and git repository. And the clone works: all the code is now available, version controlled, in my Pythonista filesystem, as you can see in the sidebar below:

![Sidebar containing a hyper-h2 folder](https://lukasa.co.uk/images/pythonista/hyper_h2.png)

This is pretty big! Essentially I now have access to every pure-Python module that has ever been published, fully executable, on my iOS device. And they work too. Some quick investigation revealed that even somewhat unexpected things work: for example, the curio asynchronous I/O framework for Python 3.5+ runs unmodified, implying that sockets, selectors, and even TLS behave as expected. All of my HTTP/2 toolchain runs as well, meaning that I was able to whip up a quick HTTP/2 client in pure-Python using curio and hyper-h2 and that was capable of doing a complete HTTP/2 request from my iPad, as you can see below:

![The curio script I ran](https://lukasa.co.uk/images/pythonista/curio_script.png)

![The output](https://lukasa.co.uk/images/pythonista/script_output.png)

## What Does This Mean?

This means that we're very close to having a fully-fledged Python programming environment on our iOS devices. The advantages of this are pretty substantial. Firstly, for those who want it, it opens up a world of scripting and automation opportunities that iOS has previously hidden away. Pythonista has a lot of hooks into the operating system that allow you to write applets or helper functions that can automate boring tasks. The folks over at MacStories have written [an enormous number of posts demonstrating some of the cool things that Pythonista can do](https://www.macstories.net/tag/pythonista/) to automate their workflows. When you add in to this the fact that there is now a fairly functional PyPI client available to obtain any helper libraries you might need, you have the ability to write almost arbitrary code that can operate on data made available elsewhere in the OS. This is an enormously powerful tool, and for anyone who is really serious about being a hardcore iOS power user it is absolutely worth investigating.

But more importantly, it's one step closer to not needing a full PC to work on Python code. For my part, I've been interested in trying to move away from needing a laptop for travel purposes. There are a number of boring reasons for this[1](https://lukasa.co.uk/2016/12/Python_on_iOS/), but ultimately my requirement has been that I needed something like a proper Python shell on an iOS device to consider swapping over to an iPad as travel computer.

Amazingly, this puts us pretty close by. An upcoming release of Stash is going to support the pip `console_scripts` extensions, which should make it possible to install and run `py.test` (my preferred testing framework). If that happens, I'll be in possession of an environment with git support and the ability to code and run my tests on the go, with no network connection required. At that point I may finally be in a position where I can do a reasonable amount of work from my iOS device.

This environment is still not perfect. There are some alarming bug reports about the git logic inside Pythonista, which means I'd rather use [Working Copy](https://itunes.apple.com/gb/app/working-copy-powerful-git/id896694807?mt=8), but it seems that right now Pythonista isn't able to treat Working Copy as a full-fledged document source. In my ideal world Working Copy would be able to expose the whole git tree to Pythonista so that Pythonista could "mount" it on the filesystem, but it doesn't immediately seem to be possible. If it became possible, I'd consider the combination of those two applications as being pretty close to the "killer app" for Python development on iOS.

Regardless, this is one of the most exciting discoveries I've made in a long time. I'm able to write genuine Python code to interact with my iOS device without needing to build an entire app to do it. This drastically reduces the overhead in scripting my operating systems, which is a huge leap forward in terms of flexibility.

It also opens a neat world of physical computing. As anyone who knows about [computing education](http://ntoll.org/) can tell you, physical computing is enormously important for educating children in computation because it provides them with direct feedback, demonstrating the utility of computing in an immediate manner. This is commonly done for smaller children with devices like the [BBC Micro:bit](http://microbit.org/), but for older children the most obvious device to use is their phone. For a long time, Android devices have been the easiest devices to use for this, but it's good to see that iOS devices are now open to being used in this way.

This is very cool, and I'm really looking forward to seeing what the community does next.
