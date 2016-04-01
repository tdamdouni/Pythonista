#!/bin/bash

if [ "$1" == "" ] ; then
    echo ""
    echo "Usage: MarkdownifyInstagram.sh {{IFTTT_Read_Path}}, {{Draft_Write_Path}}, {{Local_Image_URL_Path}}, {{Website}}, {{MarkdownifyInstagram_Path}}"
	echo "Example (for manual usage): ./PATH/TO/SCRIPT/MarkdownifyInstagram.sh /home/blog/secondcrack/www/media/instagram/ /home/blog/Dropbox/Blog/drafts/ /media/instagram/ http://jayhickey.com"
    echo "Example (or automated inotify usage): ./PATH/TO/SCRIPT/MarkdownifyInstagram.sh /home/blog/secondcrack/www/media/instagram/ /home/blog/Dropbox/Blog/drafts/ /media/instagram/ http://jayhickey.com /home/blog/Dropbox/Blog/scripts/MarkdownifyInstagram/"
    echo ""
    exit 1
fi

IFTTT_Read_Path="$1"
Draft_Write_Path="$2"
Local_Image_URL_Path="$3"
Website="$4"
MarkdownifyInstagram_Path="$5"
FORCE_CHECK_EVERY_SECONDS=30
UPDATE_LOG=/tmp/instagramUpdate.log

SCRIPT_LOCK_FILE="${MarkdownifyInstagram_Path}/MarkdownifyInstagram.pid"
BASH_LOCK_DIR="${MarkdownifyInstagram_Path}/MarkdownifyInstagram.sh.lock"

if mkdir "$BASH_LOCK_DIR" ; then
    trap "rmdir '$BASH_LOCK_DIR' 2>/dev/null ; exit" INT TERM EXIT

	python "$MarkdownifyInstagram_Path"MarkdownifyInstagram.py "$IFTTT_Read_Path" "$Draft_Write_Path" "$Local_Image_URL_Path" "$Website"

    if [ "`which inotifywait`" != "" ] ; then
        while true ; do
           	inotifywait -q -q -e moved_to -e create -e close_write "$IFTTT_Read_Path"
			python "$MarkdownifyInstagram_Path"MarkdownifyInstagram.py "$IFTTT_Read_Path" "$Draft_Write_Path" "$Local_Image_URL_Path" "$Website"
        done
    fi

    rmdir "$BASH_LOCK_DIR" 2>/dev/null
    trap - INT TERM EXIT
else
   echo "Already running"
fi