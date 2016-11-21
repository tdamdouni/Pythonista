# coding: utf-8

# https://forum.omz-software.com/topic/2868/no-sound-on-iphone6/8

import speech
import time

speech.say("English (United States)", "en-US")
time.sleep(3)
speech.say("English (Great Britain)", "en-GB")
time.sleep(3)
speech.say("English (Australia)", "en-AU")
time.sleep(3)

