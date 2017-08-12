# Why learn Python?

_Captured: 2016-03-29 at 00:05 from [medium.com](https://medium.com/p/6a21070659b1)_

![](https://cdn-images-1.medium.com/max/2000/1*UJXl_da5ah_e52zou3PLIA.jpeg)

#### from stranger in a strange land to familiar with the language

Software shapes much of my life. If you're reading this, it shapes much of yours, too. It wasn't until I joined a software startup that I realized how little about software I understood. I share the highlights from my journey into software programming here. In the beginning, I felt much like the baby fish who asks the wiser fish about the sea:

![](https://cdn-images-1.medium.com/max/800/1*Ha_Su8NHW2b7MWuVeOfHLA.jpeg)

> _[Zen Speaks](http://www.amazon.com/Zen-Speaks-Tsai-Chih-Chung/dp/0385472579)_

Once aware of it, I began to suspect my blindness to the force around me-to its [power](http://a16z.com/2014/08/25/a16z-podcast-ben-and-marc-explain-practically-everything-part-1/), to its [possibilities](https://en.wikipedia.org/wiki/Moore%27s_law), to its influence, to its boundaries-was a headwind to my career in technology. Headwinds are bad. Paul Ford's essay [What Is Code](http://www.bloomberg.com/graphics/2015-paul-ford-what-is-code/) hit me in the face as if it were a newspaper flying through a storm.

To explore nature, you take a trip into the wilderness. To explore software, you take a trip into a software programming language. What is Python? Python is a programming language that makes computers do magical things.

> It's also an interpreted, object-oriented, high-level programming language with dynamic semantics. -- [Python.org](https://www.python.org/doc/essays/blurb/)

So I dove in. Fortunately, I had two wiser fish to help me along the way. [Raylu](https://github.com/raylu) is a colleague who wrote his own Python tutorial series and who suggested I level-down and try [@AlSweigart](https://twitter.com/AlSweigart)'s [Automate the Boring Stuff](https://automatetheboringstuff.com). Professor John Mamer (PM) is in a league of his own within the faculty at [@uclaanderson](https://twitter.com/uclaanderson). He helped me with my first bug, and provided insightful context to seemingly minor things, like the difficulties of getting Python into my PATH, and to larger ideas about teaching and learning. PM pushed me to think of a program that I would want to code so that I would have a focal point and a context for my studies. I share more about this program-and what I learned from writing it-below. While I didn't study Python to understand the Dao, my way around this modern world is clearer now.

### # set up for a bunch of setup

I've spent a good bit of time wrenching on cars. PM has, too. He and I both came to realize how similiar wrenching is to coding. If you want to change your car's air filter, you'll need a few things at hand to get this done. A place to work on the car. Tools. The new air filter. Coding is the same way. These are five basic questions I had right away:

_What is a text editor, how is it different from IDLE's interactive shell, what is Terminal?_Put simply, these reference "the garage." It's where you code!

_What is a data type?_Turns out coders spend a lot of time thinking about different data types; like the difference between "G" and "7." It's obvious when written out, but you can't take G and multiply it by 7.

_What is the DRY principle?_It stands for Don't Repeat Yourself. It's a powerful, and difficult, ethos with practical benefits in coding. It leads to code that is not redundant, to code that has fewer bugs and bugs that are easier to fix, and to code that is cleaner and easier to read. It's also a very surprising goal to adopt in ones day-to-day life. If you're doing a task which is very repetitive, it's likely a software program (which is, by nature, very good at repetition) can help you out! PM pointed out that the New York Times published an interesting piece on the programmer's approach to self improvement: [cold, hard rationality](http://www.nytimes.com/2016/01/17/magazine/the-happiness-code.html?_r=0).

_What is a Library, and is it a Module?_The difference, [if there is one](http://stackoverflow.com/questions/19198166/whats-the-difference-between-a-module-and-a-library-in-python), doesn't really matter. That doesn't mean these aren't important… in fact they are absolutely crucial! Think of modules as the new air filter for your car: it's a component/part which you can place into your code. Very many libraries/modules are open-sourced, ready and free for you to use in your programs. [Requests](http://docs.python-requests.org/en/master/#), [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/), and [Selenium](http://selenium-python.readthedocs.org) are good examples.

_Where do I begin?_If this were a kitchen, you'd want the pots, knife, cutting board, and avocados [all in the right place](https://youtu.be/GgiK-HWKPjw). If this were a garage, you'd want the car in the lift, the hood open, and the tools ready. In my case, this meant [installing the latest version of Python](https://www.python.org/downloads/). And so much more, such as [upgrading pip](https://pip.pypa.io/en/stable/installing/) (which sort of serves the same purpose as your transportation to and from your favorite auto parts store).

Fortunately, simply by walking yourself through the process of getting your machine ready to start coding, you yourself will be much farther along than it seems even before writing your first line of code. You'll have run things from the command line, you'll have read through your first batch of programmer instructions, you'll have thought about software packages and versions. And you'll have taken the first step out of the graphical user interface world and made changes to the substrata of your computer that don't easily meet the eye. All of this builds confidence and familiarity, even if both are hard to spot at this early stage.

Characterizing this stage as "early" isn't the same thing as "easy." If you run into problems, like I did, it's good to remember you are not alone:

> I spent most of the day yesterday searching for a clear answer for installing pip. I can't find a good solution.

My pip problem centered on Python 2.7.10 versus Python 3.5.1:

![](https://cdn-images-1.medium.com/max/800/1*2w71f-TWYDEC7vPAG7bWdQ.png)

> _This is Terminal.app, the application that accepts command line prompts.Note I am running Python 2.7.10 here._

![](https://cdn-images-1.medium.com/max/800/1*BD6muVnJ_a1eYVnlYGv9tw.png)

> _Ah, that's better! Note that I am running Python 3.5.1 here. Versions make a difference in certain cases, like when the flavor of pip you're trying to run requires Python 3.5.1. Thanks to ben for the guidance on this one!_

#### learnings from setup

Software programming requires patience. There is a lot of readme file reading. If you are, like me, someone who skims instructions, you will quickly course correct this terrible habit. Reading, and executing, the instructions very carefully, step by step, is really the only way to do a thing successfully.

PM and I discussed the concept of clarity in communication. Have you ever left a meeting thinking everyone was on the same page? The Slack message you sent out memorializing the key action items, next steps, and folks responsible was acknowledged. Yet the next time your team pulls up to review progress, the only thing that's clear is that things have slipped sideways!

Certain types of folks will think this learning is dead obvious, others will hear it but won't listen. I wasn't listening until I hit the same roadblock a few times and finally, after what felt like a patronizing read of the instructions, followed them carefully. I found my readme religon:

![](https://cdn-images-1.medium.com/max/800/1*srYXVWfQi6haeln_8Ft_-w.png)

> _My first open-source contribution on GitHub (thanks Raylu for suggesting I send it in)! Fairly low-rent, as it's just fixing a typo in the readme. My friends from C|A would agree; sharp proofreading skills are both a blessing and a curse in daily life. Turns out proofreading is super helpful when coding._

When PM first began coding 40 years ago, access to reference material was super limited. He describes it as a small coup when the business school at UCLA convinced Hewlett Packard to donate a copy of the instruction manual for the school's mainframe computer…the manuals, all lined up, measured 8 feet wide. Back then, help was person-to-person.

> "You'd find someone who could do stuff that you couldn't do, and you'd make yourself a polite pest." -- PM

The idea of a lone programmer tucked away in a dark room somewhere hammering away on the keyboard is no longer close to reality. GitHub, Stack Overflow, [IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat), email, the internet, and tools like Slack haven't necessarily changed [the degree of collaboration](http://www.atariarchives.org/deli/homebrew_and_how_the_apple.php), but rather the periodicity, ease, and speed of it.

![](https://cdn-images-1.medium.com/max/800/1*JOJxgDJEF2HLfUIt8T2NNQ.png)

> _Ralyu provided pivotal advice in a few spots!_

### # be mindful of warnings and error messages…

…and read the readme files! Similar to how the navigation app Waze tends to kick out seemingly ignorable warning messages such as "Watch out! Pothole ahead…" certain components in your software garage will beep, buzz, and hiss at you from time to time (often in text that appears purposefully composed to make a beginner's eyes glaze over). Here is one example I delayed in addressing and that took a few hours to unravel once I finally stopped to take care of it:

> WARNING: The version of Tcl/Tk (8.5.9) in use may be unstable. Visit <http://www.python.org/download/mac/tcltk/> for current information.

AYE! Who wants anything in their system to be unstable?! The diligent don't.

If you spend any time whatsoever coding, you will find yourself exploring bugs and workarounds on [Stack Overflow](http://stackoverflow.com). It's a website where other coders mercifully help each other out. A few hours into my efforts to update Tcl/Tk and I finally found the answer I needed, as the last reply on a long thread:

![](https://cdn-images-1.medium.com/max/800/1*NO28ejrouwoU3wzXBjrRdA.png)

> _The more time you spend bug bashing, the better you'll be at spotting solutions that fit your situation._

Don't get discouraged by answers that start with "this is easy…" when you're finding it to be terribly difficult! What drew me to this reply was that it referenced PATH (a problem I had encountered before), it referenced a chart (suggesting to me this problem depends on the interesction of other variables), and it did not involve reinstalling Python (something I was loathe to attempt).

There are also warnings in many of the instructions you'll come across as you start to try new things with the code, or as you delete and update programs. A particularly scary example for me came from my decision to skim the following Mozilla page for instructions on how to delete a saved Firefox web browser profile:

![](https://cdn-images-1.medium.com/max/800/1*1rh4CJOgwtrxWEXhwE6csA.png)

Resist the urge to read the instructions completely until finding what you think you're looking for. Don't qualify completely with "until I find what I'm looking for." What comes later might be important! In other words, completely actually does mean completely. #duh

#### learnings from warnings

If you look closely at the screenshot-closer than I looked [at the page](https://support.mozilla.org/en-US/kb/profile-manager-create-and-remove-firefox-profiles)-you'll notice the special warning section towards the bottom. I navigated to that page to find out how to delete profile files, and spotted the relevant instructions towards the top. What I didn't see was that this Mozilla tool will delete both the files and the folder in which the Firefox browser profile is stored.

My issue was that I had stored the Firefox browser profile in the same folder as my latest version of the code for my program. Might as well keep your directories tidy, right? Thankfully, I had backed up the program code on Google Drive. Lesson learned…delete stuff very carefully and read instructions thoroughly!

As I shared with PM how careful attention to warnings was curing a lot of issues, he pointed out the power of context. Font, capitalization, spacings, tab indents, and punctuation are mission critical to functional code. Experience with these issues and time spent resolving exceptions and addressing warnings provide an invaluable, intangible context to code. Of course, context plays an important role in other situations. One example that comes to mind is the [Commanding Officer's Intent](http://www.fireleadership.gov/toolbox/briefing_intent/Shattuck.pdf), which is a concept in military leadership circles used to guide the behavior of soldiers.

### # writing code

Yes, the first script I wrote included printing "[Hello World!](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program)" (typically the first stroke taken in the ocean of programming).

![](https://cdn-images-1.medium.com/max/1200/1*T5Xn9gmOCxbhtH2PjCI6AQ.png)

> _I've gone a little crazy here with the # comments (which Python ignores) to help explain within the code what each line of actual code actually does._
