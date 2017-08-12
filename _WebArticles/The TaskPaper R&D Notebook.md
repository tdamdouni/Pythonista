# The TaskPaper R&D Notebook

_Captured: 2015-09-30 at 17:54 from [www.macdrifter.com](http://www.macdrifter.com/2014/02/the-taskpaper-rd-notebook.html)_

This is part two in the series. [In part one](http://www.macdrifter.com/2014/01/deconstructing-my-omnifocus-dependency.html), I discussed the rules and detail designs of a plain text based task management experiment. The tag and project structure in the TaskPaper format is flexible and easy to comprehend. But the system is only as good as the tools available for working with the documents.

In this article, I'll document a broad set of tools available on various platforms for working with TaskPaper documents. This will not be a description of the "ideal" but rather a catalog of options. Some work very well and some are unsatisfying.

I'll also mix-in some of my own custom tools and conclude with a small initiative to help expand on the available tools.

If you are looking for a solution, this is not it. If you are looking for my R&D notes, then you're at the right address.

## The Tools

One of the great things about plain text systems like TaskPaper is that pretty much any application that can read and write txt files can do the basics. The downside is that most tools _just_ do the basics.

I'm attempting to string together many disparate applications and scripts to accomplish what OmniFocus does with a single platform.[1](http://www.macdrifter.com/2014/02/the-taskpaper-rd-notebook.html) Some solutions work almost perfectly without any tweaking but on iOS, it's a Sisyphean feat to have full control over a task list.

I'll lay out what I've found and how I'm attempting to use it below.

### Alarming Events

Let's clear this up right away. TaskPaper and similar apps are not active tools. They don't grab you any more than a paper notebook would. While OmniFocus incorporates alerts at a basic level, it's never been my preferred tool for reminders. I've always found OmniFocus to be too passive and easily dismissed (or missed) to rely on the notifications.

I've used Due.app on [Mac](https://itunes.apple.com/us/app/due/id524373870?mt=12&uo=4&at=11l5Ug) and [iOS](https://itunes.apple.com/us/app/due-super-fast-reminders-reusable/id390017969?mt=8&uo=4&at=11l5Ug) for quite awhile. There's a lot to like about Due. It has terrific plain-english syntax and flexible repeat reminders. Because the apps all sync through Dropbox or iCloud, I'm much more likely to get the message.

Due.app also has a great URL scheme which means that it can integrate well with Drafts or Editorial.

There are also a few downsides to Due.app. The syncing requires me to open the app on iOS periodically. It's not a terrible burden, but also not ideal.

Second, Due is outside of my other scheduling apps, like calendars and Outlook. It's nice having a place to see everything in the coming week all at once.

It's also not easy to segregate and categorize all of the reminders in the Due app. Some are for work and some are for personal tasks. But in Due, it's just one long list of everything.

Apple's Reminders.app is a viable alternative to Due.[2](http://www.macdrifter.com/2014/02/the-taskpaper-rd-notebook.html) It integrates with various calendar apps, including Outlook by way of Exchange. With apps like [Fantastical](https://itunes.apple.com/us/app/fantastical-2-calendar-reminders/id718043190?mt=8&uo=4&at=11l5Ug), I can use plain English to enter an alert. Reminders syncs across iOS, Mac and Exchange and includes a web app option when all else fails.

![](http://www.macdrifter.com/uploads/2014/01/2014-01-26%2020.52.36_350px.png)

The Reminders app provides enough customization for repeating tasks and includes options for location based reminders, which I rarely use.

![](http://www.macdrifter.com/uploads/2014/01/2014-01-26%2020.51.17_350px.png)

The big benefit to Reminders is that I can categorize groups of reminders and share them with my wife. While I appreciate the complex repeating options available in Due.app, I'll probably stick with Reminders.app for all of the other reasons, not to mention that **it's pretty hard to miss an alert from Reminders**.

![](http://www.macdrifter.com/uploads/2014/02/2014-02-01%2018.07.28_650px.png)

### TaskPaper for Mac

This falls into the "Almost Perfect" category. Being the origin of the format, the [Mac application](http://www.hogbaysoftware.com/products/taskpaper) TaskPaper supports all of the syntax I need. Through AppleScript, anything that's not immediately available can be added.

TaskPaper obviously shares it's streamlined interface with the closely related Mac app, WriteRoom, from the same developer. The interface is sparse, which is a nice change from many of the toolbar laden apps I've worked with. While the basic themes in TaskPaper are pleasant, they feel a little dated. I've switched to the excellent [HelvetiCan Theme](https://gist.github.com/tundramonkey/5056539).

![](http://www.macdrifter.com/uploads/2014/02/Screen%20Shot%2020140201_120411_400px.jpg)

#### TaskPaper Query Language

The single most powerful feature of TaskPaper is the smart search which replicates and exceeds "Perspectives" in OmniFocus. Using the logical and powerful query syntax, it's possible to slice and dice a large task list at will.

![](http://www.macdrifter.com/uploads/2014/01/Screen%20Shot%2020140123_200913_650px.jpg)

The syntax is a combination of natural language and attribute flags. The TaskPaper documentation describes it as an attribute search term relationship:
    
    
    <attribute> <relation> <search term>
    

For example, to limit the view to a single project, use the obvious project Trash Compactor Malfunction or use a the attribute syntax project=Trash Compactor Malfunction. You can also use the relation operator "contains" for more general queries like project contains Trash to find all projects that contain the word "Trash".

Working with tags is equally flexible. Any tag, including completely arbitrary tags, can be search. For example, given some tags like @parsecs(1) @parsecs(2) you can construct an apparently logical query like @parsecs < 2 to find all tasks and projects with an @parsecs tags with attributes less than 2.

An extremely valuable option is to negate a specific tag. For example I generally append not @done to a most queries so that I do not see the tasks or projects that are complete.

Date attributes are also valuable search options in TaskPaper and respond to boolean syntax such as @start < 2014-02-02.

![](http://www.macdrifter.com/uploads/2014/02/Screen%20Shot%2020140202_101757_400px.jpg)

Through combinations of search terms and attribute relations, there's a huge variety of options in TaskPaper to evaluate a project or a day's activities. Here's some that I've found particularly useful:

In Progress Tasks:
    
    
    not @done and not @cancel and not @hold and (@started or @draft or @waiting or @today)
    

Stalled Tasks:
    
    
    not @done and not @cancel and (@hold or @waiting)
    

Available Tasks:
    
    
    not @done and not @cancel and not @hold and (@start <=  2014-02-02 or @due <=  2014-02-02 or @today)
    

All Tasks and Projects with a due date (+d shows descendants as well):

#### Saved Searches in TaskPaper for Mac

The most significant drawback to TaskPaper for Mac is that it lacks the ability to save and organize these smart searches. Luckily, there are a few solutions.

First, are TextExpander shortcuts. Expand a shortcut to instantly narrow the task list. There's more power here that an initial glance might suggest. TextExpander has excellent support for time-stamp math which opens an entirely new level of sophistication in TaskPaper queries.

I've mapped the "Available Tasks" query about to the following TextExpander shortcut:
    
    
    not @done and not @cancel and not @hold and (@start <=  %Y-%m-%d or @due <=  %Y-%m-%d or @today)
    

This is simple enough. The date placeholders are expanded to today's current date.

Here's a variant to show all items available soon:
    
    
    not @done and not @cancel and not @hold and (@start <= %@+5D%Y-%m-%d or @due <=  %@+5D%Y-%m-%d or @today)
    

This uses the TextExpander date math to expand the date for 5 days in the future and limits the TaskPaper list to all items with an @due or @start date less than or equal to that date.

#### Diversion: TextExpander

One of the easiest ways to get around the lack of saved searches in TaskPaper is through the use of TextExpander snippets. This is a basic filter for late tasks. It uses the TextExpander date functions to look for anything tagged with a @due date of today or earlier.
    
    
    not @done and not @cancel and not @hold and @due <=  %Y-%m-%d
    

This snippet is useful for checking on Available Tasks:
    
    
    not @done and not @cancel and not @hold and (@start <=  %Y-%m-%d or @due <=  %Y-%m-%d or @today)
    

Here's a TextExpander snippet for tasks and projects that will be available in the next 5 days. It uses the Date Math function to automatically enter the date 5 days in the future:
    
    
    not @done and not @cancel and not @hold and (@start <= %@+5D%Y-%m-%d or @due <=  %@+5D%Y-%m-%d or @today)
    

Any of these snippets can be applied on the fly and combined with other search terms. So, if you want to look at overdue tasks on a specific project, just enter project contains Trash followed by the snippet shortcut.

![](http://www.macdrifter.com/uploads/2014/01/Screen%20Shot%2020140123_202718_400px.jpg)

#### More Options for Controlling TaskPaper

I've employed Keyboard Maestro as a helper application for some my more obscure saved searches.[3](http://www.macdrifter.com/2014/02/the-taskpaper-rd-notebook.html) Rather than write TextExpander snippets and create separate macros, I use KM to enter the TE snippets. The macro group is pretty simple in functionality. It activates TaskPaper and expands the snippet in the search field.

TaskPaper is a highly scriptable application. I've discovered that almost anything I want to accomplish is accessible through AppleScript. Just browse through the TaskPaper [AppleScript Wiki](http://www.hogbaysoftware.com/wiki/TaskPaperAppleScripts) to get an idea of the wide variety of tools being developed to work with the application.

[There's a script](http://www.hogbaysoftware.com/wiki/UseSiriWithTaskPaper) to move tasks from a Reminders list into TaskPaper. Or how about [moving tasks from TaskPaper](http://macintoshguy.wordpress.com/2013/01/09/taskpaper-to-reminders-applescript-version-two/) to the Reminders app? If you're a BusyCal user, then grab the [TaskPaper to BusyCal bundle](https://github.com/glvnst/time_management/blob/master/taskpaper2busycal.py).

There's a [Script to convert TaskPaper entry types](https://github.com/jeredb/taskpaper-applescript-benoit). Or if you want to go full-nerd then check out the [Taskpaperparser project](https://code.google.com/p/taskpaperparser/) which converts a TaskPaper document into an AppleScript "object" for manipulating the entire project/task model.

I've see [many scripts](http://www.lawschoolmatt.com/uncategorized/more-on-applescript-dates-and-taskpaper) and workflows for handling automatic date conversion and updating of due tags.

The TaskPaper format is so flexible and easily parsed that entire [time tracking systems](http://www.hogbaysoftware.com/wiki/TimeTracking) have been built off of it. I think you get the idea. The sky's the limit when you're working with plain text.

This is an area that benefits from the flexibility of the TaskPaper format. Since tags and attributes are completely free-form in TaskPaper, I've been able to create ad-hoc grouping of tasks and projects:
    
    
    Death Star: @review(weekly)
    Hoth Probe: @review(weekly)
    The Ewok Infestation: @review(weekly)
    

TaskPaper also provides quick entry of new items through system input panel available with the hotkey combination ⇧+⌘+⏎. This integration goes a long way at replacing the OmniFocus inbox on the Mac.

![](http://www.macdrifter.com/uploads/2014/02/Screen%20Shot%2020140202_165831_400px.jpg)

But of course, there are alternatives through helper applications like Alfred. [Here's an Alfred Workflow](http://dropbyte.tumblr.com/post/21794666472/taskpaper-meets-alfred-update-2-1) for adding and accessing tasks. [Pedro Lobo also brings us](https://github.com/pslobo/Scripts/tree/master/Alfred%20App/TaskPaper%20Extended%20Notes) a clever extension of the TaskPaper notes functionality but accessible through Alfred.

Clearly the Alfred entry point for TaskPaper is a popular one. This [TaskPaper for Alfred](http://da.rryl.me/projects/taskpaper/) package goes one step further and creates a "bump" action to move a task's due date to tomorrow. It also provides some GeekTool functionality.

Rob Trew began providing scripts for converting plain text lists to OmniFocus [back in 2012](http://www.macdrifter.com/2012/02/plain-text-to-omnifocus.html). I have a suspicion that we'll start see tools from him that move items the other direction in 2014.[4](http://www.macdrifter.com/2014/02/the-taskpaper-rd-notebook.html)

Brett Terpstra has been working with TaskPaper for several years and has developed little utilities like his [TaskPaper logger for Day One](http://brettterpstra.com/2012/02/25/automating-taskpaper-to-day-one-logs/) and his [Next Actions CLI](http://brettterpstra.com/2012/11/17/next-actions-cli-updated-time-to-meet-the-parents/) for working with TaskPaper from the command line.

#### Folding Text

There's also TaskPaper's cousin, FoldingText for Mac. While FoldingText supports the tags in TaskPaper, it is really designed for working with Markdown. There is no easy way to focus on a project or tag in Folding Text.

However, it's clear that Folding Text is the future for TaskPaper. The development version of Folding Text has received significant updates and is built on a much more flexible text filtering model. There's even [a new SDK available](http://www.foldingtext.com/sdk/). My money is on Folding Text replacing TaskPaper in the coming months. I also believe this will be a major step forward in plain text task management, given Folding Text's central focus is on text editing with time management features added on top.

![](http://www.macdrifter.com/uploads/2014/02/Screen%20Shot%2020140202_175228_650px.jpg)

### Notes

As I mentioned in my previous post, notes in a the TaskPaper format are far more expressive and valuable than in many other systems that I've tried. My task list contains many more details and bits of reference material than I ever put into OmniFocus. I believe that this results from the in-line editing and display of notes. I also believe this has increased my preparation efforts while decreasing the time I spend getting ready to execute on a task.

### Sublime Text

Sublime Text with the [PlainTasks package](https://github.com/aziz/PlainTasks) is a serviceable task manager with TaskPaper formatted text files. It's not as efficient as the TaskPaper Mac application but there are some basic features that make it a very useful tool. It's worth noting that the package receives regular updates and it works on Mac, Windows and Unix.

![](http://www.macdrifter.com/uploads/2014/01/Screen%20Shot%2020140127_184948_450px.jpg)

The PlainTasks package is popular and I've seen several useful forks and additions. [Jonathon Poritsky](https://github.com/poritsky/PlainTasksOF) put together a nice alternative styling to PlainTasks that's worth installing.

Because Sublime Text has powerful search features, it's fairly easy to keep on top of tasks. Just hit Shift+ctrl+F and search for a tag to get a clickable perspective-like view.

![](http://www.macdrifter.com/uploads/2014/01/Screen%20Shot%2020140127_185041_450px.jpg)

But there are major shortcomings too. There's no direct way to filter by start or due dates or to focus on a single project. You can perform the following regular expression search to narrow the view a bit:
    
    
    @due\(2014\-[01|02]\-\d\d\)
    

This finds "@due" tags with dates of January or February of this year. This could be done with smart TextExpander snippets but it's just slightly awkward on Windows.

One nice feature of Sublime Text's PlainTasks is the project folding implementation. It's nice to quickly expand and collapse sections of a larger file.

There are several shortcuts in the PlainTasks bundle that make working with TaskPaper files convenient. Hitting ^+d appends the @done tag with the current date stamp. Hitting alt+c will append the @cancel tag.

Type s,tab,tab to mark an item as @started or t,tab,tab to mark a task for @today

The PlainTasks package also provides a clean-up function. Hit the shortcut ⌘+⇧+a to archive @done tasks to the bottom of the current file and adds an @project tag that indicates the original source project that it came from.

![](http://www.macdrifter.com/uploads/2014/02/Screen%20Shot%2020140202_194020_450px.jpg)

Sublime Text provides a couple of generic functions that work well with the PlainTasks package. Hitting ^+r displays a list of all projects and selecting one from the list instantly jumps to that point.

The ^+⇧+f search option in Sublime Text is convenient for creating Perspective-like views of tasks. Search on @today to get a list of just the tasks for today.

![](http://www.macdrifter.com/uploads/2014/02/Screen%20Shot%2020140202_194300_450px.jpg)

I've added the folder with my task files as a project in Sublime Text, so I get the added benefit that the "Search in Files" command automatically highlights results in all of my TaskPaper documents.

You can also use the standard Sublime Text tools to manipulate tasks. The ^+⇧+up or down functions can move a line (task or project) up or down in the file.

Perhaps with some additional plugins, Sublime Text will become a full-fledged tool for TaskPaper formatted files, but it is a bit rough right now. To that end, I've been developing some of [my own Sublime Text functions](https://github.com/macdrifter/SublimeTaskFunctions/blob/master/README.md) that make it a bit easier to quickly show available tasks and projects in the current TaskPaper file.

Just last week Pedro Lobo unveiled a [MailMate plugin](http://plobo.net/mailmate-bundle-for-taskpaper) based on AppleScript examples from Ryan Lane. This plugin sends the currently selected message in MailMate to either the front-most TaskPaper document or a predefined document. As a huge fan of [MailMate](http://freron.com/), I like the direction this is going and shows some of the promise of this format for building custom tools.

#### GeekTool

[GeekTool](http://projects.tynsoe.org/en/geektool/) is a popular utility for displaying content on the desktop. Of course there is significant overlap between the kind of person that uses TaskPaper and the kind that uses GeekTool. The [TaskPaper Parser project](https://github.com/kmarchand/TaskPaper-Parser) puts some of your tasks on your desktop.

The older set of scripts that are part of the [GeekTool TaskPaper XML parser](http://www.hoboes.com/Mimsy/hacks/geektool-taskpaper-and-xml/) laid a great foundation that seems easy to work off of for a variety of purposes.

### iOS

#### TaskPaper

For iOS, TaskPaper is still the ideal solution. This is a problem, given that development and support has been discontinued. The best features in TaskPaper are the smart search-and-filter options as well as quick tag and project filtering.

![](http://www.macdrifter.com/uploads/2014/01/2014-01-23%2013.19.28_350px.png)

But there are still major holes in the applications. Similar to TaskPaper for Mac, there's no option to save a smart search for repeated use. One solution is to leverage the TaskPaper URL scheme from apps like LaunchCenter Pro. But remember in part one when I suggested using separate files for each area of obligation? That's a problem for TaskPaper search since it's not a global function.

This **could** be solved with judicious use of TextExpander, if only TaskPaper supported the new TextExpander API. [Here's a workaround](http://blog.jeffreykishner.com/2013/12/29/usingLaunchCenterProToUseTextexpanderSnippetsInTaskpaperForIos.html) that uses LaunchCenter Pro to open TaskPaper and place the TextExpander snippet for a query on the clipboard but this is really a short lived solution.

![](http://www.macdrifter.com/uploads/2014/01/2014-01-23%2013.23.41_350px.png)

But, unless you already purchased TaskPaper for iOS, you can no longer get it. It's gone from the App Store.

My conclusion is that TaskPaper for iOS was once a great start. But it's lost its luster and has now been abandoned by the developer. Unfortunately, there is nothing that fully replaces it yet. There are some early opportunities but a long road ahead my deter customers looking for a replacement.

#### Listacular for iPhone

[Listacular](https://itunes.apple.com/us/app/listacular-for-dropbox-rapid/id624606571?mt=8&uo=4&at=11l5Ug) is the heir apparent to TaskPaper on iOS and is recommended by the TaskPaper developer. As of this writing, it is not a replacement. It lacks all of the query features and smart syntax of TaskPaper. It is currently just a smart list manager, albeit a very nice one. It includes features for easily rearranging items and added due dates but there is little else for working with a complex task list.

![](http://www.macdrifter.com/uploads/2014/01/2014-01-26%2020.47.54_350px.png)

The Listacular developer is working on bringing the app up to the TaskPaper feature list but it's hard to recommend it for anything more than quickly viewing and adding tasks at this point.

#### Editorial for iPad

[Editorial for iPad](https://itunes.apple.com/us/app/editorial/id673907758?mt=8&uo=4&at=11l5Ug) does not natively support TaskPaper, but can be twisted into a fairly competent tool. If you insist on using the TaskPaper file extension, you can configure Editorial to recognize the files. I use the .txt file extension, like a reasonable person.

I've built several Editorial workflows to specifically process the TaskPaper format. [This macro](http://www.editorial-workflows.com/workflow/5867653860163584/8Sn5h11LES4) scans all files in the folder for the currently open file and displays tasks or projects with @due, @start dates of today or earlier. It also includes items with the @today tag. It excludes items that contain the @done tag.

![](http://www.macdrifter.com/uploads/2014/02/2014-01-31%2019.45.01_800px.png)

I've created a [workflow for quickly inserting tags](http://www.editorial-workflows.com/workflow/5826400699285504/uKc9xWfVGjM) by compiling a list of all tags in all files and displaying an alphabetical list. Choose one to insert at the current cursor position.

![](http://www.macdrifter.com/uploads/2014/02/2014-01-26%2011.50.03_650px.png)

Or [focus on a particular tag](http://www.editorial-workflows.com/workflow/5249066900389888/tmTb6BsvyKA) by choosing it from a list of all tags and showing tasks that contain a match.

Finally, here's [a similar workflow](http://www.editorial-workflows.com/workflow/6378385601200128/5xA7j1qvP6k) that shows a list of all projects in all files. Select one from the list to get a summary search result set that matches the project name.

[Derrick Fay also has several workflows](http://dfay.fastmail.fm/et/) to replicate the TaskPaper workflow in Editorial.

On iOS, Editorial is proving to be the best solution for me. That might be a result of my level of comfort with creating new workflows but I'm very impressed with what can be accomplished with this file format in a very short time.

I'm looking forward to a day when the TaskPaper query syntax can be enabled by an Editorial workflow. That might be my ideal working environment.

#### Drafts

It's no surprise that [Drafts](https://itunes.apple.com/us/app/drafts/id502385074?mt=8&uo=4?mt=8&uo=4&at=11l5Ug) for iOS makes an excellent quick capture tool for plain text task lists. I've configured several actions for prepending tasks to my existing project files.

![](http://www.macdrifter.com/uploads/2014/01/2014-01-26%2021.02.23_350px.png)

This creates a new entry at the top of the text file that looks like this:
    
    
    - Get the Tie Fighter services @added(2014-01-27)
    
    Palpatine's Birthday Party: @start(2014-01-25) @due(2014-02-13)
        Dinner party reservation:
            - Lookup Regal Beagal's phone number
            - Tally guest count
            - Book party @due(2014-02-05)
            - Confirm dinner party @due(2014-02-10)
    

In a small way, my disappointment in OmniFocus 2 for iPhone prepared me for this workflow. Since I ultimately only used it for quick capture, I don't feel a strong desire to find a fully functional task manager for my iPhone.

#### Text Editors for iPhone

Because my TaskPaper documents are text files, I have the advantage of using any of my preferred text editors on my iPhone to search and edit my tasks. My primary requirements are that they provide a search option and arbitrary Dropbox navigation. I need the ability to move between my normal notes and task list and I don't want to use multiple text editors.

[Notesy](https://itunes.apple.com/us/app/notesy-for-dropbox/id386095500?mt=8&uo=4&at=11l5Ug): Quick access with global search.

[Nebulous Notes](https://itunes.apple.com/us/app/nebulous-notes/id375006422?mt=8&uo=4&at=11l5Ug): Nice editor with macros and customizable keyboard.

[Write for iPhone](https://itunes.apple.com/us/app/write-for-iphone-beautiful/id587363157?mt=8&uo=4&at=11l5Ug): An attractive editor with a Markdown-centric keyboard

WriteRoom for iPhone was one of the best, but it's been retired along with TaskPaper.

Byword has too many Dropbox sync errors to be useful.

#### Outliner Apps

Since these files are just plain text, I thought that a general purpose outliner app might be a useful way browse and edit. I was wrong. [CloudOutliner](https://itunes.apple.com/us/app/cloud-outliner-outlining-tool/id542911846?mt=8&uo=4?mt=8&uo=4&at=11l5Ug) can not import and export in plain text. [CarbonFin Outliner](https://itunes.apple.com/us/app/outliner/id284455726?mt=8&uo=4?mt=8&uo=4&at=11l5Ug) mangles the indentation when exporting and adds dashes in front of projects. [OmniOutliner for iPad](https://itunes.apple.com/us/app/omnioutliner-2/id704610906?mt=8&uo=4&at=11l5Ug) does not provide an easy way to convert a plain text list to an outline. It was worth a shot.

I also tried [Workflowy](https://workflowy.com) but the formats were not perfectly compatible.

#### Pythonista

[Pythonista](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8&uo=4&at=11l5Ug)

[Here's another gem from Pedro Lobo and Phillip Gruneich](https://gist.github.com/pslobo/f89cb16d4ad384c9fc9f). It's a Pythonista script for propagating the @done tags to all sub-tasks in a completed project.

There are additional options listed under the Miscellaneous sections that also apply to Pythonista.

#### Additional Options

Phillip Gruneich has been developing [some interesting alternatives](http://philgr.com/blog/tasks-for-today-from-taskpaper-to-begin) for use on the iPhone that rely [Launch Center Pro](https://itunes.apple.com/us/app/launch-center-pro/id532016360?mt=8&uo=4&at=11l5Ug).

### Miscellaneous Tools and Scripts

I've discovered that there are many different reasons _why_ people use the TaskPaper format, but there are an equal number of ways that they use it too. There's some truly impressive work out there. Most of it requires an intense desire for a particular solution and the technical knowledge to make it work. But if you want a good starting point, you could do worse than starting with these projects:

[TaskPyper](https://code.google.com/p/taskpyper/) is an early Python based project for working with TaskPaper files. It's a good reference source but has not been developed since 2008.

The [Python-TaskPaper](https://github.com/mattd/python-taskpaper) project has been stagnant for 4 years but also provides a basis for working with TaskPaper documents.

[SyncTasks](https://github.com/Darchangel/SyncTasks) is a Python based project for syncing TaskPaper with several other task management services, such as Google tasks.

[Jerry Straton's web display of TaskPaper](http://www.hoboes.com/Mimsy/hacks/web-display-taskpaper/) is an interesting predecessor to other browser based implementations.

[Folding for TaskPaper](http://hugowetterberg.github.io/folding/) generates an HTML version of a TaskPaper document for use in a web page. It's a clever way to share the progress of a development project.

[TaskPaper+](https://github.com/MrBertie/taskpaperplus) looks to be a web app for working with TaskPaper files but feels like a mess. The GitHub page points to a Web site that is filled with pop-up ads. You should probably stay away.

[TodoPaper](http://widefido.com/products/todopaper/) is apparently a Windows alternative to TaskPaper. It looks like it is using the same syntax and reserved tags. I haven't tried it but it would be my second option, after Sublime Text.

[TaskPython-Web](https://code.google.com/p/taskpython-web/) is a little python project for serving up TaskPaper files on a web server. This might be a lightweight way to go for interacting with TaskPaper files on an iPhone using Pythonista.

The [Dropbox Taskpaper Editor](https://github.com/thrashr888/dropbox-taskpaper-editor) looks like the holy grail but I was unable to get it functioning. It claims to be a web application that provides a full TaskPaper workflow and connects to your own Dropbox account. It requires an app key (which I generated). My intention was to get this running in Pythonista for iPhone or at least setup on my own web server. It's certainly an impressive piece of work.

[TodoFlow](https://github.com/bevesce/TodoFlow) (a.k.a. Topy) is an incredible CLI implementation for TaskPaper files. It's impressive for it's support of the TaskPaper query syntax as well as the detail it generates at the bash prompt. But if that weren't enough, there are Alfred and GeekTool extensions built off of it to provide a unified working environment all based on the TodoFlow scripts.

And just to show off, the developer "[bevesce"](https://github.com/bevesce) includes a Pythonista version of the script.

[JQuery.taskpaper](https://github.com/toddb/jquery.taskpaper) is just what you think. It's a JQuery, browser-based parser for TaskPaper formatted text.

### Conclusion

There are a lot of smart people dedicated to the TaskPaper format and they have been for a long time.

Intellectual lock-in is hard to see while grinding away day after day with the same tool. Looking at what's been done with this format over the years I see a huge variety of interpretations all built on some basic principles. TaskPaper is the idea, not the tool.

If you are interested in collaborating with some of the smart people that are using TaskPaper, contact them or me. I've gathered a few folks on Glassboard that are actively working on extending the TaskPaper toolkit. If you're looking to help, you are most welcome to stop by.

### References

There's a lot of links in this post. Here's a complete list of references:

  1. <http://www.macdrifter.com/2014/01/deconstructing-my-omnifocus-dependency.html>
  2. [https://itunes.apple.com/us/app/due/id524373870?mt=12&uo=4&at=11l5Ug](https://itunes.apple.com/us/app/due/id524373870?mt=12&uo=4&at=11l5Ug)
  3. [https://itunes.apple.com/us/app/due-super-fast-reminders-reusable/id390017969?mt=8&uo=4&at=11l5Ug](https://itunes.apple.com/us/app/due-super-fast-reminders-reusable/id390017969?mt=8&uo=4&at=11l5Ug)
  4. <http://simplicitybliss.com/blog/a-few-remindersapp-tips-tricks-applescripts>
  5. <https://github.com/macdrifter/SublimeTaskFunctions/blob/master/README.md>
  6. <http://blog.jeffreykishner.com/2013/12/29/usingLaunchCenterProToUseTextexpanderSnippetsInTaskpaperForIos.html>
  7. [https://itunes.apple.com/us/app/editorial/id673907758?mt=8&uo=4&at=11l5Ug](https://itunes.apple.com/us/app/editorial/id673907758?mt=8&uo=4&at=11l5Ug)
  8. <http://www.editorial-workflows.com/workflow/5867653860163584/8Sn5h11LES4>
  9. <http://www.editorial-workflows.com/workflow/6378385601200128/5xA7j1qvP6k>
  10. [https://itunes.apple.com/us/app/cloud-outliner-outlining-tool/id542911846?mt=8&uo=4?mt=8&uo=4&at=11l5Ug](https://itunes.apple.com/us/app/cloud-outliner-outlining-tool/id542911846?mt=8&uo=4?mt=8&uo=4&at=11l5Ug)
  11. [https://itunes.apple.com/us/app/pythonista/id528579881?mt=8&uo=4&at=11l5Ug](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8&uo=4&at=11l5Ug)
  1. To be fair, not even OmniFocus has feature parity across the platforms. There are still only context specific perspectives on iOS and they only recently added global search on the iPhone. [↩](http://www.macdrifter.com/2014/02/the-taskpaper-rd-notebook.html)

  2. Check out [Sven's list](http://simplicitybliss.com/blog/a-few-remindersapp-tips-tricks-applescripts) of tips and links for Reminders.app. [↩](http://www.macdrifter.com/2014/02/the-taskpaper-rd-notebook.html)

  3. Who can remember all of those perspectives they create, let alone all of the TextExpander shortcuts. [↩](http://www.macdrifter.com/2014/02/the-taskpaper-rd-notebook.html)

  4. There's already plenty of OmniFocus export options [available right now](https://github.com/psidnell/ofexport). [↩](http://www.macdrifter.com/2014/02/the-taskpaper-rd-notebook.html)
