# learn-math
# https://omz-forums.appspot.com/pythonista/post/5826815734054912
# https://github.com/blmacbeth/learn-math

blmacbeth on 20 Feb 2015

As some of you may have seen, I have been trying to dynamically load classes from a subfolder (or any folder...). It has been for a maths learning app I have started developing for my wife (she is studying for the GRE). I am using some simple, single view "sub-app(?)" that I developed to help build some basic math skills that we tend to forget as we get out of practice: partners to ten; multiplication; subtraction; etc.

Anyway, the way the app works is that it looks through the games subfolder and imports all of the py and pyui files, except for those in list (a file in the future) of ignored files. It then adds them to a list and sends that list to a ui.ListDataSource object to display on screen.

The main view is simply ui.TableView and that is displayed in a ui.NavigationView. When you click on a Game to play, and press the play button at the bottom of the screen, the ui.View is pushed on the navigation view.

I have been trying to find a better way to import the views dynamically, but for now the app works and games can be added very easily. This app is made for the iPhone and may look silly on screens larger than the iPhone6. I encourage you to fork my repository, clone, whatever, and play around with it. If you have ideas for new games, implement them and add them to the games folder; they will automatically be added to the app.

I am particularly proud of my Dice Game, I am going to be using the basic idea for some other apps.

I do plan on further development of this little app and I hope to see some great ideas from you on learning maths. I will also be adding a description to each game in the docstrings for each one. If you plan on submitting/adding a game, please add a doctoring description.

Please let me know what you think, not only about the app, but overall design (I'm not terribly well practiced at software engineering...).

B

EDIT: I've added some abilities, most notably the ability to add info on how to play by adding a doc string.