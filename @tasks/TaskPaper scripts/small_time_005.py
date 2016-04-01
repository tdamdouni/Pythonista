""" Functions for translating informal dates to TaskPaper format """
#coding: utf-8

TXT_SAMPLE = "- This is an action with relative tags @due(tomorrow) \
@start(yesterday) .\n\
- and here is another with other tags @due(now) @start(today) @pause ."

TXT_SAMPLE2 = "- This is an action with absolute tags @due(2014-02-15) \
@start(2014-02-13) .\n-and here is another with \
other absolute or dateless tags \
@due(2014-02-14 13:19) @start(2014-02-14) @pause ."

SCRIPT_NAME = 'SmallTime date/time translator and updater'
DESCRIPTION = 'Converts informal time expressions adjustment in tags \
                to standard TaskPaper format'
AUTHOR = 'Rob Trew'
VER = '.05'
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

# import workflow

import re
from datetime import datetime, timedelta
from tokenize import generate_tokens
from StringIO import StringIO

TPL_ANCHORS = ('now', 'yesterday', 'today', 'tomorrow')
TPL_SENSE = ('+', '-')
TPL_ABBREV = ('y', 'w', 'd', 'h', 'm')
TPL_UNITS = ('years', 'weeks', 'days', 'hours', 'minutes', 'year', \
    'week', 'wk', 'wks' 'day', 'hour', 'hr', 'hrs', 'minute', 'mins')
TPL_POSTANTE = ('am', 'pm', 'a', 'p')
STR_MONTHS = 'janfebmaraprmayjunjulaugsepoctnovdec'

RGX_KV_TAG = r'\@(\w+)\(([^\)]+)\)'
RGX_TP_DATE = r'\d{4}-\d{2}-\d{2}'

def main():
    """Testing only"""
#    str_tag = workflow.get_variable('str_input_tag')
#    workflow.set_output(update_tag(str_tag))
#    print tag_updates(TXT_SAMPLE2)

    print "Text with translations and date deferrals automatically applied:\n"
    print "FROM :", TXT_SAMPLE
    print "TO (start & due +4d):", defer_dates(['start', 'due'], \
        '+4d', TXT_SAMPLE), '\n'
    print "FROM :", TXT_SAMPLE2
    print "TO (start only -1w): ", defer_dates(['start'], '-1w', TXT_SAMPLE2)
    print '\n', examples()

def examples():
    """Sample of expressions which can be translated"""
    lst = ['today +7d', '11:20 +4d', '2014-02-15 +1w', 'jan 10', \
    'jan 10 2pm', '10 jan at 10am', 'now-3d', '+7d', '7', '11:15',\
     '11:15p', '11p', 'aug', 'jan 5', 'aug 2019', 'now', "tomorrow 2pm",\
      "now +4h", 'today + 1w', '1w', '+3y', 'w', '1w']
    for tpl in zip(lst, [phrase_to_datetime(str_e) for str_e in lst]):
        print tpl


def defer_dates(lst_tag_types, str_delta, str_txt):
    """ lst_tag_types:
            list of one or more key strings (without @)
            ['due', 'start']
        str_delta:
            positive or negative time delta
            '+7d' or '-2w'  etc
        str_txt:
            lines of text assumed to include some @key(datevalue) tags

        returns (dct_defer, str_defer)
        dct_defer:
            keys : types of tag which have been deferred / brought forward
            values : numbers of that kind of tag deferred / brought forward
        str_defer:
            the changed version of the text (deltas applied to tag dates)

        Apply a time delta  to all tags of the specified kind(s)
        in the text. (exclude @s from lists of tag types)
        Return a dict with counts for each type of updated tag,
        and the updated text.
        USE CASES:
        - Update all tags in the selected range
        - if no tags were updated, offer a list of date tag types
          - if selection(s) made:
          - prompt for delta (+3d +4w -1w etc)
        - apply the specified delta to all tags of the specified type(s)
    """
    if (lst_tag_types != []) and (str_delta != '') and (str_txt != ''):

        # build and compile a regex matching the specified tags
        # group(1) = tag key, group(2) = tag value
        str_rgx = ''.join([r'\@(',
          '|'.join(lst_tag_types),
          r')\(([^\)]+)\)'])

        # and loop through any matches
        str_defer = ''
        i_prev = 0
        dct_defer = dict()
        rgx_tags = re.compile(str_rgx)
        for o_match in rgx_tags.finditer(str_txt):
            (i_start, i_end) = o_match.span()
            str_tag_key = o_match.group(1)
            str_tag_value = o_match.group(2)
            str_update = ''.join([
              '@', str_tag_key, '(',
              phrase_to_datetime(str_tag_value + str_delta),
              ')'
            ])

            # record a deferral of this kind of tag
            if str_tag_key not in dct_defer.keys():
                dct_defer[str_tag_key] = 0
            dct_defer[str_tag_key] += 1

            # and build the translated string
            str_defer = ''.join([str_defer, str_txt[i_prev:i_start], \
              str_update])
            i_prev = i_end

        if dct_defer:
            str_defer = ''.join([str_defer, str_txt[i_prev:]])
        else:
            str_defer = ''

        return (dct_defer, str_defer)


def tag_updates(str_txt):
    """ Returns a tuple:
        1.  A dict of each tag type updated, with count
        2.  A unique set of date tag types found but not updated
        3.  If there have been updates, the updated string
    """

    str_trans = ''
    i_prev = 0
    dct_deltas = dict()
    lst_unchanged = []

    rgx_date = re.compile(RGX_TP_DATE)
    rgx_tag = re.compile(RGX_KV_TAG)
    for o_match in rgx_tag.finditer(str_txt):
        (i_start, i_end) = o_match.span()
        str_group = o_match.group()
        str_update = update_tag(str_group)
        str_tag_key = o_match.group(1)
        if str_update != str_group:
            if str_tag_key not in dct_deltas.keys():
                dct_deltas[str_tag_key] = 0
            dct_deltas[str_tag_key] += 1
        else:
            # if the value includes a TP date pattern
            if rgx_date.search(o_match.group(2)) != None:
                lst_unchanged.append(str_tag_key)

        str_trans = ''.join([str_trans, str_txt[i_prev:i_start], \
          str_update])
        i_prev = i_end

    if dct_deltas:
        str_trans = ''.join([str_trans, str_txt[i_prev:]])
    else:
        str_trans = ''

    return (dct_deltas, set(lst_unchanged), str_trans)


def update_tag(str_tag):
    """    Try to return a date translated/updated
            version of a TaskPaper tag
    """
    str_key, str_value = tp_key_value(str_tag)
    var_result = phrase_to_datetime(str_value)

    if var_result is not None:
        str_trans = var_result
    else:
        str_trans = str_value

    if str_trans != '':
        lst = [' @', str_key, "(", str_trans, ")"]
    else:
        lst = [' @', str_key]

    return ''.join(lst)


def tp_key_value(str_tag):
    """ Extract a key and a value from a string
        assumed to be a TaskPaper tag
    """
    rgx_split = re.compile(r'[\@\(\)\{\}]')
    str_key, str_value = '', ''

    # count the pieces
    lst_parts = rgx_split.split(str_tag)
    lng_parts = len(lst_parts)

    # and winnow the noise
    if lng_parts > 1:
        str_key = lst_parts[1]
        if lng_parts > 2:
            for str_value in lst_parts[2:]:
                if str_value != '':
                    break

    return (str_key, str_value)

def phrase_to_datetime(str_phrase):
    """Informal phrase to TaskPaper format"""
    return _tp_fmt(rel_date(str_phrase))



def up_date(dte, r_quant, str_unit, bln_post_colon):
    """    Adjust a date in the light of a (quantity, unit) tuple,
          taking account of any recent colon
    """
    if str_unit == 'w':
        dte += timedelta(weeks=r_quant)
    elif str_unit == 'd':
        dte += timedelta(days=r_quant)
    elif str_unit == 'h':
        dte += timedelta(hours=r_quant)
    elif str_unit == 'm':
        dte += timedelta(minutes=r_quant)
    elif str_unit in ('Y', 'y'):
        if r_quant > 500: # jul 2019 vs jul 17
            r_year = r_quant
        else:
            r_year = datetime.now().year + r_quant
        try:
            dte = datetime.replace(dte, year=int(r_year))
        except ValueError:
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
    elif (len(str_unit) >= 3) and (STR_MONTHS.find(str_unit) != -1):
        dte = datetime.replace(dte, month=(STR_MONTHS.index(str_unit) + 3)/3,
            day=int(r_quant), second=0, microsecond=0)
        # refers to this year or next year ? (assume not past)
        dte_today = datetime.today().replace(hour=0, minute=0, \
          second=0, microsecond=0)
        if dte < dte_today:
            dte = dte.replace(year=(dte_today.year+1))
    return dte

def rel_date(str_date):
    """    Translate a relative or informal date expression
          into a Python datetime struct,
          or return the string unchanged if it can't be parsed
    """

    bln_date = False
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
            bln_date = True
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
            else:
                str_tkn_lower = str_tkn.lower()
            if str_tkn in TPL_ANCHORS:
                bln_date = True
                if str_tkn != 'now':
                    dte = dte.replace(hour=0, minute=0, second=0, \
                      microsecond=0)
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
                dte = up_date(dte, r_quant, 'H', bln_post_colon)
                str_unit = 'M'
                bln_new_unit, bln_new_quant = True, False

            elif is_num(str_tkn):
                bln_date = True
                r_quant = float(str_tkn) * lng_sense
                lng_sense = 1 # negative sign only affects one number
                if r_quant > 2000 and r_quant < 2500:
                    if bln_new_unit:
                        dte = up_date(dte, 1, str_unit, bln_post_colon)
                    str_unit = 'Y'
                    bln_new_quant, bln_new_unit = True, True
                else:
                    bln_new_quant = True

            elif (str_tkn in TPL_ABBREV) or (str_tkn in TPL_UNITS):
                bln_date = True
                str_unit = str_tkn[0]
                bln_new_unit = True

            elif str_tkn_lower in TPL_POSTANTE:
                str_unit = str_tkn[0]
                bln_new_unit, bln_new_quant = True, True

            elif STR_MONTHS.find(str_tkn_lower) != -1:
                bln_date = True
                str_unit = str_tkn_lower
                bln_new_unit = True

            if bln_new_unit and bln_new_quant:
                bln_date = True
                dte = up_date(dte, r_quant, str_unit, bln_post_colon)
                bln_new_unit, bln_new_quant = False, False

        # default unit is day, default quantity is 1
        if bln_new_unit and (not bln_new_quant):
            bln_date = True
            dte = up_date(dte, 1 * lng_sense, str_unit, bln_post_colon)
        elif (not bln_new_unit) and bln_new_quant:
            bln_date = True
            dte = up_date(dte, r_quant, 'd', bln_post_colon)

    if not bln_date:
        dte = None
    return dte


def extract_date(str_date):
    """    Find the first %Y-%m-%d string
          and return any legitimate datetime
          with the remainder of the string
    """
    rgx = re.compile(r'((\d{4})-(\d{2})-(\d{2}))')
    o_match = rgx.search(str_date)
    if o_match is not None:

        lng_day = int(o_match.group(4))
        lng_month = int(o_match.group(3))
        lng_year = int(o_match.group(2))

        # These digits may not give a legitimate combination of Y M D
        try:
            dte = datetime(lng_year, lng_month, lng_day)
        except ValueError:
            # Use today's values as defaults, and use any part that does work
            dte = datetime.now()
            # Start with day=1 in case the month is feb and the day 30 etc
            dte = datetime.replace(dte, day=1, hour=0, minute=0, \
              second=0, microsecond=0)
            try:
                dte = datetime.replace(dte, year=lng_year)
            except ValueError:
                pass
            try:
                dte = datetime.replace(dte, month=lng_month)
            except ValueError:
                pass
            try:
                dte = datetime.replace(dte, day=lng_day)
            except ValueError:
                pass

        i_start = o_match.start()
        tpl_date_rest = (dte, str_date[0:i_start] + ' ' + \
          str_date[i_start + 10:])

    else:
        tpl_date_rest = (None, str_date)

    return tpl_date_rest

def is_num(str_token):
    """Numeric token ?"""
    try:
        float(str_token)
        return True
    except ValueError:
        return False

def _tp_fmt(var):
    """Convert to TaskPaper date format if this is a datetime"""
    if type(var) is datetime:
        if var.hour == 0 and var.minute == 0:
            str_out = var.strftime('%Y-%m-%d')
        else:
            str_out = var.strftime('%Y-%m-%d %H:%M')
    else:
        str_out = var
    return str_out

if __name__ == '__main__':
    # examples()
    main()
