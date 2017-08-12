# The Movie Diary with Airtable and Pythonista

_Captured: 2016-03-26 at 19:46 from [onetapless.com](https://onetapless.com/new-movie-diary-with-airtable)_

I have an itch to tweak my workflows until they're perfect only to break them apart and start all over again, and with the [Movie Diary](https://onetapless.com/actions/workflow/movie-diary), my favorite and most used action, I was unsatisfied with [Day One](https://itunes.apple.com/us/app/day-one-2-journal-+-notes/id1044867788?mt=8&uo=4&at=10l4KL) as a log keeper for habitual stuff, because every log template organizes data that would fit better in a database and that's not what makes a great journaling app, which Day One is.

After the release of Day One 2.0 I started looking for alternatives, [Momento](https://itunes.apple.com/us/app/momento-diary-journal/id980592846?mt=8&uo=4&at=10l4KL), another journaling app, couldn't format MultiMarkdown tables nor accept the poster from an URL scheme call, making it a step backwards. [Evernote](https://itunes.apple.com/us/app/evernote/id281796108?mt=8&uo=4&at=10l4KL) would also lack the benefits from using a database (I'm also glad not to use it anymore). [Microsoft Excel](https://itunes.apple.com/us/app/microsoft-excel/id586683407?mt=8&uo=4&at=10l4KL) or [Numbers](https://itunes.apple.com/us/app/numbers/id361304891?mt=8&uo=4&at=10l4KL) would give me database-like sorting and filtering, I just wouldn't be able to insert data from iOS. Then in [Viticci's 'New Apps for 2016'](https://www.macstories.net/roundups/new-apps-for-2016/) roundup I was introduced to [Airtable](https://itunes.apple.com/us/app/airtable-flexible-database/id914172636?mt=8&uo=4&at=10l4KL), a mix of spreadsheet and visual database that would be the perfect place for the kind of data we want to log in the Movie Diary.

## Configuring Airtable

Airtable is a webservice with a native app available for iOS, it allows you to sort, filter and connect entries in the database with a layout that adapts to whatever device you're on. The first step is to create a new database, these are the required steps on the iOS app:

  1. Tap the _New base_ button;
  2. Select _Create a new empty base_;
  3. Name your database;
  4. Tap the big circular plus button in the bottom-center;
  5. In the card view, you'll get the default fields (Name, Notes and Attachments). Tap _Customize..._ in the bottom-left corner;
  6. Rename _Name_ to _Title_;
  7. Rename _Notes_ to _Overview_;
  8. Rename _Attachments_ to _Poster_;
  9. Add a new Single Line Text field named _Rating_;
  10. Add a new Single Line Text field named _Directors_;
  11. Add a new Single Line Text field named _Year_;
  12. Add a new Date field named _Date_;

You should reorder the fields to provide most important information at glance, for example, I use _Title_ followed by _Rating_, so when I'm visualizing the entries on the iPhone I can see these fields and the poster. You can also rename the table, The name of your database and the name of your table is not relevant to configure this workflow, so you can customize those as you like.

Now we gotta setup your API and, unfortunately, the experience is not consistent across mobile platforms and you'll face difficulties setting up the API on a mobile device, for example, attempting to login on a mobile device will open the app in the App Store. You can fake a desktop browser on iOS with [iCab Mobile](https://itunes.apple.com/us/app/icab-mobile-web-browser/id308111628?mt=8&uo=4&at=10l4KL):

  1. Tap the cog wheel icon to open the "Settings" panel;
  2. Tap "Web Sites";
  3. Tap "Browser ID";
  4. Change "Default Browser ID" to the latest Mac version (Safari 7.1 (Mac)).

Whenever you're ready to configure the API, log in from the [API page](https://airtable.com/api) (available at the footer), log into your account, choose your newly created database and you'll go to a full documentation page customized to your database, I want you to look at the URL, it should look like `https://airtable.com/<random string>/api/docs#curl/introduction` and I want you to save that `<random string>` bit for later (use [Drafts](https://itunes.apple.com/us/app/drafts-4-quickly-capture-notes/id905337691?mt=8&uo=4&at=10l4KL), [Clips](https://itunes.apple.com/us/app/clips-copy-paste-anywhere/id917638056?mt=8&uo=4&at=10l4KL) or [Copied](https://itunes.apple.com/us/app/copied-copy-paste-everywhere/id1015767349?mt=8&uo=4&at=10l4KL)). Here you'll realize that you could set whatever name pleased you for the fields, but for the sake of simplicity, you should stick with mine for now.

Still in the documentation in your desktop environment, tap the _Open Base_ link in the top-right corner (or just open your Dashboard any other way). Look up the name of the table in the bottom-left corner, it should be _Table 1_, but you can change it, if you do, don't forget to setup in the script accordingly. Click the people icon in the top-right corner and select _Account_ in the dropdown, near the bottom you'll find a _Generate API key_ link, tap it, copy the string it provides and save it for later.

## Configuring Pythonista

Are you still here? The worst part is over and you're welcome to enter Valhalla with your API and database keys. You're welcome to run the script, if you got the [New from Gist](https://onetapless.com/actions/pythonista/new-from-gist) script a while ago, this will be a smooth installation.

The first time you run the script you'll be prompted 4 times for configuration. The first prompt is for the MovieDB API key and is comes pre-filled with my token, which you were already using in the previous version; you can set your own MovieDB API key or just continue the script. After finding and selecting a movie you'll be asked to insert your Airtable API key (the one that starts with _key_), then the database ID and finally the name of the table, prefilled with _Table 1_ unless you renamed it earlier. Pick a rating and you'll receive a HUD alert indicating if the entry was successfully added. You'll never be asked for these credentials on this device again.

Whatever you log, I think [Airtable](https://itunes.apple.com/us/app/airtable-flexible-database/id914172636?mt=8&uo=4&at=10l4KL) is a formidable tool with a good API to explore and [Pythonista 2.0](https://geo.itunes.apple.com/us/app/pythonista/id528579881?mt=8&uo=4&at=10l4KL) with its action extension made me return to Python as a way to solve problems on iOS. Now go watch some movies and get used to these apps as we're going to see this combo again soon.

## Troubleshooting

Can I import my entries from Day One?
    Not possible, sorry, you gotta do it manually. Here's something to help you: Uncomment line 76 and comment line 77, now you'll get a datepicker dialog while adding movies. We could perhaps build a tool for OSX if we get enough interest, but it took me around 1 hour to manually add all my entries, and I have a lot of them. This is a good reason to move to Airtable since it exports databases in CSV format.
I misconfigured, how do I reset the keys and tokens?
    You can run [this script](https://gist.github.com/philgruneich/ad8e62c2b7b7ad1b7a7a) to overwrite the configuration, it will prefill each field with the current stored value so you can only update the field you want, if you renamed the table or something.
Why am I getting an _Failed to Connect_ error?
    First check if you're not offline, then update to the [latest version](https://gist.github.com/philgruneich/72f2fb734dcaf404cf36) of the script. If all fails, send me an [email](mailto:phil@onetapless.com) or a [DM on Twitter](https://twitter.com/onetapless) so we can work this out, still covering every possible error in this scenario and the message is pretty much boilerplate only.
Why am I getting an _Invalid Data_ error?
    Most of the time this happens due to date formatting. The script is configured by default to include only the date to your entries, not the time. If you're unsure, open your database, then an entry and go to Customize Fields, edit the Date field and look for the _Include a time field_ toggle, turn it off if you don't need the time. If you want to have the time in the database, remove `.date()` from line 77 and replace `date_dialog()` in line 76 for `datetime_dialog()`.
How can I add the time to the date of my entries?
    Check the previous answer.
My problem is not listed here.
    [E-mail](mailto:phil@onetapless.com) or [tweet](https://twitter.com/onetapless) my way.
