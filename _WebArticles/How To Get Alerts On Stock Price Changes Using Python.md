# How To Get Alerts On Stock Price Changes Using Python

_Captured: 2016-04-10 at 13:43 from [www.movingelectrons.net](http://www.movingelectrons.net/blog/2014/01/12/how-to-get-alerts-on-stock-price-changes-using-python.html)_

## Overview

There are several services and Apps out there which alert you when stock prices change. However, some of them don't issue alerts soon enough, are highly unreliable or provide limited customizability. I wanted to have more control over the process and be able to modify the settings on the go. I also wanted to get alerts _within at least 15 min of the price change_.

I came up with the solution that has been working with no problems for at least a year. If for some reason I cannot get the instant message in my phone (because I'm traveling with no data connection or in a plane), I can rely on having an email in my inbox notifying me of the stock price change. I'm not a stock broker, so I don't really need to be informed of stock changes the minute they happen, but I just like to know relatively quick if things are going south. I may tweak the script down the road to make it more _intelligent_ and to improve exception handling. If I do it, I'll update this post.

## What Is Needed?

There is the software, hardware and services needed:

  * Python Script.
  * [Dropbox account](https://db.tt/LdFyqgz2).
  * An always-on machine running Python (I have a small Linux server running my Python scripts).
  * [Pushover App for iOS](https://itunes.apple.com/us/app/pushover-notifications/id506088175?mt=8&uo=4&at=11lqkH).
  * SMTP email service. I'm using the free gmail's SMTP server. [Here](https://support.google.com/mail/answer/78775?hl=en) is a link to Google's support pages showing the server name and port that you need to use (you can also see it in the Python script).

## How Does It Work?

![Alerts on Stock Price Changes](http://www.movingelectrons.net/images/Stock_Script.png)

The key is having the script running at regular intervals (in my case, it runs every 15 minutes). There are many ways to achieve this. Since mine is running on a Linux box, I'm using _Cron_ for that, more specifically it's GUI interface (more info [here](https://help.ubuntu.com/community/CronHowto)).

## The Python Script

**Full Disclaimer:** _I don't consider myself a programmer. Although I did program in several languages in college, that was some time ago. I'm pretty sure you can find some better and more efficient ways to achieve the same results. If you do, feel free to revise the code. However, I can assure you that the script works just fine as it is right now._

You can grab the script from GitHub [here](https://gist.github.com/Moving-Electrons/8387168). I have included comments in key lines and where the code may get a little confusing. These are actually comments to myself since I wasn't planning to post the script or make it public in any way when I wrote it.

The script's logic is fairly simple: it takes a text file as an argument and reads the stock symbol, trigger value and the condition ( _a_ for above and _b_ for below ) from each line in the file. If the condition is met, then it sends an email to a predetermined email address and sends a _push_ notification to your cellphone (in this case, an iPhone) through [Pushover](https://itunes.apple.com/us/app/pushover-notifications/id506088175?mt=8&uo=4&at=11lqkH).

So, let's say we want to get notified when Apple stock rises above $500. We would include the following line in the text file:

`AAPL,500,a`

Note that the script is case sensitive and all symbols should be in CAPS.

The reason the text file is passed as an argument, is because I wanted to keep the script as portable and versatile as possible so it would be easy to run it through a different configuration file. **Therefore, what runs every 15 minutes is actually a shell script that calls the python script with the text file as an argument.**

The shell script has a single line:

`python /PATH_TO_SCRIPT/StockAlert.py /PATH_TO_DROPBOX_FOLDER/Symbols.csv`

Make sure to make the shell script executable (instructions [here](http://stackoverflow.com/questions/817060/creating-executable-files-in-linux)).

Since the text/csv file is in a dropbox folder, it can be accessed from computers and mobile devices. So if it is modified in another device (say, your phone), Dropbox would sync the changes to the always-on machine and your script would take the updated text file as an argument.

The pushover credentials (see below), email credentials and SMTP email server info is hard-coded in the script and you will need to enter them in **lines 39, 40 and 47 to 53**.

## Pushover Configuration

Once you download Pushover from the [iTune Store](https://itunes.apple.com/us/app/pushover-notifications/id506088175?mt=8&uo=4&at=11lqkH), go to the developer [page](https://pushover.net), signup for the service and obtain your **User Key** and create a **Token** for your application (in this case, the script). You can also assign an icon to each application so it would show when getting the alert on your phone.

## Putting It All Together

If you got everything set up correctly, you should be able to test the whole workflow by adding some lines to the Symbols.csv file in the following format:

`SYMBOL,price,trigger`

Therefore, adding the line in the example above to check Apple stock price would produce the following results:

![Pushover Screenshot](http://www.movingelectrons.net/images/Pushover_Screenshot_2.jpg)

![Pushover Screenshot](http://www.movingelectrons.net/images/Pushover_Screenshot_1.jpg)

Additionally, you would receive an email like the following:

![Pushover email](http://www.movingelectrons.net/images/email_screenshot.png)
