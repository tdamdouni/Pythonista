
SCRIPT_NAME = 'SmallTime - Very Small Relative Datetime Language'
DESCRIPTION = 'Translates relative and informal date/time expressions into \
                standard TaskPaper format'
AUTHOR = 'Rob Trew'
VER = '.02'
LICENSE = """Copyright (c) 2014 Robin Trew

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE."""

import re, time
from datetime import datetime, timedelta
from tokenize import generate_tokens
from StringIO import StringIO


TPL_ANCHORS = ('now', 'yesterday', 'today', 'tomorrow')
TPL_SENSE = ('+', '-')
TPL_ABBREV = ('y', 'w', 'd', 'h', 'm')
TPL_UNITS = ('years', 'weeks', 'days', 'hours', 'minutes',
    'year', 'week', 'wk', 'wks' 'day', 'hour', 'hr', 'hrs', 'minute', 'mins')
TPL_POSTANTE = ('am', 'pm', 'a', 'p')
STR_MONTHS = 'janfebmaraprmayjunjulaugsepoctnovdec'

def phrase_to_datetime(str_phrase):
    return _tp_fmt(rel_date(str_phrase))

def examples():
    lst = ['today +7d', '11:20 +4d', '2014-02-15 +1w',  'jan 10', 'jan 10 2pm', '10 jan at 10am',
        'now-3d', '+7d', '7', '11:15', '11:15p', '11p', 'aug', 'jan 5',
        'aug 2019','now', "tomorrow 2pm", "now +4h",
            'today + 1w', '1w', '+3y', 'w', '-w']
    for tpl in zip(lst, [phrase_to_datetime(str_e) for str_e in lst]):
        print tpl

def update(dte, r_quant, str_unit, bln_post_colon):
    """Adjust a date in the light of a (quantity, unit) tuple,
       taking account of any recent colon"""
    if str_unit == 'w':
        dte += timedelta(weeks=r_quant)
    elif str_unit == 'd':
        dte += timedelta(days=r_quant)
    elif str_unit == 'h':
        dte += timedelta(hours=r_quant)
    elif str_unit == 'm':
        dte += timedelta(minutes=r_quant)
    elif str_unit in ('Y','y'):
        if r_quant > 500: # jul 2019 vs jul 17
            r_year = r_quant
        else:
            r_year = datetime.now().year + r_quant
        try:
            dte = datetime.replace(dte, year=int(r_year))
        except:
            dte = datetime.replace(dte, day=28, month=2,
                year=int(datetime.now().year + r_quant))
    elif str_unit == 'H':
        dte = datetime.replace(dte, hour=int(r_quant), second=0, microsecond=0)
    elif str_unit == 'M':
        dte = datetime.replace(dte, minute=int(r_quant),
            second=0, microsecond=0)
    elif str_unit == 'a':
        if not bln_post_colon:
            dte = datetime.replace(dte, hour=int(r_quant), minute=0,
                second=0, microsecond=0)
    elif str_unit == 'p':
        if bln_post_colon: # adjust by 12 hours if necessary
            if dte.hour < 12:
                dte = datetime.replace(dte, hour=dte.hour+12)
        else:
            p_quant = r_quant
            if p_quant < 12:
                p_quant += 12
            dte = datetime.replace(dte, hour=int(p_quant), minute=0,
                second=0, microsecond=0)
    elif STR_MONTHS.find(str_unit) != -1:
        dte = datetime.replace(dte, month=(STR_MONTHS.index(str_unit) + 3)/3,
            day=int(r_quant), second=0, microsecond=0)
        # refers to this year or next year ? (assume not past)
        dte_today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        if dte < dte_today:
            dte = dte.replace(year=(dte_today.year+1))
    return dte

def rel_date(str_date):
    """Translate a relative or informal date expression
       into a Python datetime struct.
    """

    # First extract any %Y-%m-%d base date
    str_copy = str_date
    (dte_anchor, str_copy) = extract_date(str_copy)

    # then get all remaining tokens
    lst_tkn = [tpl[1] for tpl
        in generate_tokens(
            StringIO(str_copy).readline)]

    # START WITH DEFAULT ASSUMPTIONS
    if len(lst_tkn) > 1:
        # drop an anchor (default is now failing any %Y-%m-%d in the string)


        if dte_anchor is None:
            dte_now = dte = datetime.now()
            dte = dte_now
        else:
            dte = dte_anchor
        dte = dte.replace(hour=0, minute=0, second=0, microsecond=0)

        # set a course (default +0 days)
        lng_sense = +1 # + / -
        r_quant = 0
        str_unit = "d"

        bln_new_quant = False
        bln_new_unit = False

        # AND ALLOW EACH TOKEN TO UPDATE
        bln_post_colon = False
        for str_tkn in lst_tkn:
            if str_tkn == '':
                continue
            if str_tkn in TPL_ANCHORS:
                if str_tkn != 'now':
                    dte = dte.replace(hour=0, minute=0, second=0, microsecond=0)
                    if str_tkn == 'yesterday':
                        dte -= timedelta(days=1)
                    elif str_tkn == 'tomorrow':
                        dte += timedelta(days=1)
                else:
                    dte = datetime.now()

            elif str_tkn in TPL_SENSE:
                if str_tkn == '+':
                    lng_sense = 1
                else:
                    lng_sense = -1

            elif str_tkn == ":":
                bln_post_colon = True
                dte = update(dte, r_quant, 'H', bln_post_colon)
                str_unit = 'M'
                bln_new_unit, bln_new_quant = True, False

            elif is_num(str_tkn):
                r_quant = float(str_tkn) * lng_sense
                lng_sense = 1 # negative sign only affects one number
                if r_quant > 2000 and r_quant < 2500:
                    if bln_new_unit:
                        dte = update(dte, 1, str_unit, bln_post_colon)
                    str_unit = 'Y'
                    bln_new_quant, bln_new_unit = True, True
                else:
                    bln_new_quant = True

            elif (str_tkn in TPL_ABBREV) or (str_tkn in TPL_UNITS):
                str_unit = str_tkn[0]
                bln_new_unit = True

            elif str_tkn.lower() in TPL_POSTANTE:
                str_unit = str_tkn[0]
                bln_new_unit, bln_new_quant = True, True

            elif STR_MONTHS.find(str_tkn.lower()) != -1:
                str_unit = str_tkn.lower()
                bln_new_unit = True

            if bln_new_unit and bln_new_quant:
                dte = update(dte, r_quant, str_unit, bln_post_colon)
                bln_new_unit, bln_new_quant = False, False

        # default unit is day, default quantity is 1
        if bln_new_unit and (not bln_new_quant):
            dte = update(dte, 1 * lng_sense, str_unit, bln_post_colon)
        elif (not bln_new_unit) and bln_new_quant:
            dte = update(dte, r_quant, 'd', bln_post_colon)

    return dte


def extract_date(str_date):
    """Find the first %Y-%m-%d string
       and return the datetime and the remainder of the string
    """
    rgx = re.compile('\d{4}-\d{2}-\d{2}')
    o_match = rgx.search(str_date)
    if o_match is not None:
        i_start = o_match.start()
        i_end = i_start+10
        return (datetime(
            *(time.strptime(str_date[i_start:i_end], "%Y-%m-%d")[0:6])),
            str_date[0:i_start] + str_date[i_end:])
    else:
        return (None, str_date)


def is_num(str_token):
    """Numeric token ?"""
    try:
        float(str_token)
        return True
    except ValueError:
        return False

def _tp_fmt(dte):
    if dte.hour == 0 and dte.minute == 0:
        return dte.strftime('%Y-%m-%d')
    else:
        return dte.strftime('%Y-%m-%d %H:%M')

if __name__ == '__main__':
    examples()





