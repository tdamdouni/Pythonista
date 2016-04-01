# Markdownify Instagram

Markdownify Instagram pairs with an [IFTTT Recipe](http://ifttt.com/recipes/49883) to automatically create an embedded Instagram markdown post. 

The Instagram post can also be downloaded to a local path on your server for embedding—so you don't have to rely on Instagram for hosting.

**Warning:** Markdownify Instagram is in early development. Use it with caution and at your own risk. There may be bugs—please let me know of any issues you have and I'll look into them. Feel free to pull request!

## Installation

### Setting Up IFTTT

Create this [IFTTT Recipe](http://ifttt.com/recipes/49883). Your Dropbox folder path can be whatever you want, but make sure the filename is `URL`. And the "Content" section should look exactly like this:

![IFTTT](https://raw.github.com/jayhickey/MarkdownifyInstagram/master/img/recipe.png)

 All the blue text items can be selected from the combo box on the right side or entered manually, e.g., by entering `{{Url}}` or `{{Caption}}`.

### Running Manually

`MarkdownifyInstagram.py` can be run manually by passing in the following parameters (inside the mustaches):

    python MarkdownifyInstagram.py {{IFTTT_Read_Path}}, {{Draft_Write_Path}}, {{Local_Image_URL_Path}}, {{Website}}

The last two parameters are optional. Here's a breakdown:

- `{{IFTTT_Read_Path}}` is the Dropbox folder path you chose when setting up your recipe on IFTTT. 
- `{{Draft_Write_Path}}` is the path where you want your markdown file saved.
- **Optional**: `{{Local_Image_URL_Path}}` is what folder inside `{{Website}}` that you want the locally embedded photo. It will need to be located somewhere in the root of your `{{Website}}`. 

Here's an example:

    python MarkdownifyInstagram.py /home/blog/secondcrack/www/media/instagram/ /home/blog/Dropbox/Blog/drafts/ /media/instagram/ http://jayhickey.com

**Note:** All parameters will need `/`'s at the beginning and end, except `{{Website}}`

### Running Automatically with iNotify

With [inotify-tools](https://github.com/rvoicilas/inotify-tools/wiki), you can use `inotify-wait` with the included shell script. Adding the script to your crontab will enable Instagram Automator to run automatically when a IFTTT Instagram file hits your `{{IFTTT_Read_Path}}`. 

Type `crontab -e` and add this (the last two parameters are still optional):

    * * * * * /PATH/TO/SCRIPT/MarkdownifyInstagram.sh {{IFTTT_Read_Path}}, {{Draft_Write_Path}}, {{Local_Image_URL_Path}}, {{Website}}, {{MarkdownifyInstagram_Path}}

Running Instagram Automator automatically (no pun intended) is highly recommended. IFTTT will check for new trigger data every 15 minutes, and `iNotfy-wait` will run almost instantaneously. If you use a static blogging engine and set your `{{Draft_Write_Path}}` to your publishing folder (such as the `_publish_now` folder in [Secondcrack](https://github.com/marcoarment/secondcrack/blob/master/README.markdown)), every Instagram picture can be posted to your blog as soon as IFTTT triggers.



