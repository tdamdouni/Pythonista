# Building a CMS on Editorial

_Captured: 2015-11-30 at 00:18 from [unapologetic.io](http://unapologetic.io/posts/2014/08/21/building-a-cms-on-editorial/)_

(▼)

Yesterday [I posted](http://unapologetic.io/posts/2014/08/19/ftp-client-ui-for-editorial/) on a workflow I built in [Editorial](https://itunes.apple.com/us/app/editorial/id673907758?mt=8&uo=4&at=11lpto) which pops up a user interface for connecting to a web server over FTP. That alone is quite useful to me for manipulating files already on the server, but before uploading new posts I first need to do quite a lot of work on them to get them ready to display properly on Unapologetic.

Last year I challenged myself to leave [Squarespace](http://squarespace.com) behind and write a new website from scratch (▼). After a few months of work, Unapologetic was born. Fully coding the site had the advantages of letting me add some of my favorite touches, such as the in-text footnotes and drop down share sheets, but I lost the huge convenience of Squarespace's [CMS](http://en.m.wikipedia.org/wiki/Content_management_system).

Without a CMS and with my self-written code, before posting anything to Unapologetic I have to follow these steps:

  * Convert markdown to HTML.
  * Properly format every footnote with the necessary code.
  * Add the share sheet code to the top of the file, which requires the new post's URL slug to be pasted into multiple different places within it.
  * Place specific class tags on images depending on whether they are double portrait images or single landscape images.
  * Duplicate the file and prepare one with the header and footer code for a permalink page and the other to be placed into the home page.
  * Update the RSS file with the new post's information and a short description of it.

Doing that manually is a massive pain, and very much prone to human error. As such, I wrote a script in Pythonista last year which automated the whole process. I send it a file typed in markdown which includes the title, article type, and article description on the first three lines. The script breaks the file apart, takes out the top three lines and uses them to build the URL slug, identify the article type, and save the short description for the RSS update. Next it formats any footnotes with my custom footnote code, converts the text from markdown to HTML, formats images, adds in the code for share sheets (with the URL slug inserted in the necessary positions), then creates and uploads two different files, one formatted for the home page and the other for the permalink page. Finally the actual homepage and the RSS page are updated to include the new post.

I have been using this script for nearly nine months now and it works quite well, but after uploading my files there has been no easy way to edit them or otherwise manipulate them on the server. To solve the latter problem I built my FTP client UI, and for the former (as well as for the overall simplification of my posting workflow) I built another UI called "Post to Unapologetic".

![Post to Unapologetic UI](http://unapologetic.io/images/building-a-cms-on-editorial/post-to-unapologetic-ui.png)

> _Post to Unapologetic UI_

This UI moves the process of posting to my website into a GUI, where it is far easier for me to check that I'm not making errors with the positions of the data on the first few lines. I can also tweak the article type, change the auto-created permalink if I want to, and write the description of the post last instead of first. For the most part this is just a graphical interpretation of the same script I've been using, but I've also made a few tweaks to really make it possible to use Editorial as a nearly full CMS for Unapologetic.

Each time I tap the "Post to Unapologetic" button on the UI, before changing the markdown to HTML, the script first saves another file, "md.txt", in the same folder as the new post which contains a dictionary of the post's data, including the markdown version of the text. With this file, each time I need to update a post on Unapologetic, either with new information or just to fix a typo, I open the folder with my FTP client and use a special button (▼) to open and interpret the md.txt file. It opens in Editorial with the contents of the markdown version of my post, with the relevant data such as the post's permalink, description, article type, and title in the first few lines at the top. From here I can edit my post normally and then run my Post to Unapologetic workflow once again. The workflow reads the lines placed at the top and determines that this is an update instead of a new post, then it formats the post back into its proper HTML form, including footnotes, share sheet, etc, and overwrites the old file for the permalink and home page. Since it knows the post is an update, it skips adding it into the RSS feed or home page for a second time.

With this combination of two UI workflows, I've taken a shaky, text based method for posting which had no good way to make updates or error check before uploading files live to my website, and turned it into a much more stable and easy to work with process. Editorial's UI module has allowed me to build a content management system from scratch, and this CMS runs right on top of the app which I do all of my actual writing on.

I won't post the workflow publicly because it's completely customized to this website, and thus won't be useful to anyone else in its current form. If you are interested in putting something similar together for your own website though, and wish to see my code, [ping me](http://unapologetic.io/contact) and I'll send you a link to the private workflow.

The things that iPads can do these days continue to amaze me. With the impending release of iOS 8, which brings with it Extensions and other fantastic new enhancements, I can't wait to see want the next era of iOS automation is going to look like, and look forward to my iPad gaining even more powerful abilities.
