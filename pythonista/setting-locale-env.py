# coding: utf-8

# https://forum.omz-software.com/topic/2544/wish-list-for-next-release/78

# https://forum.omz-software.com/topic/608/locale-currency-doesn-t-work

import locale
locale.setlocale(locale.LC_ALL, 'fr_FR')

import locale; locale.setlocale(locale.LC_ALL, 'de_DE')

>>> import locale
>>> loc = locale.getlocale() # get current locale
# use German locale; name might vary with platform
>>> locale.setlocale(locale.LC_ALL, 'de_DE')
>>> locale.strcoll('f\xe4n', 'foo') # compare a string containing an umlaut
>>> locale.setlocale(locale.LC_ALL, '') # use user's preferred locale
>>> locale.setlocale(locale.LC_ALL, 'C') # use default (C) locale
>>> locale.setlocale(locale.LC_ALL, loc) # restore saved locale

