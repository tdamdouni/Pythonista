"""
Set of tools to transform and interpret text in .taskpaper format.

It's used internally in todoflow but can by also useful outside of it.
"""
from __future__ import absolute_import
import re
import datetime as dt


task_indicator = '- '
project_indicator = ':'
tag_indicator = '@'

# Types


def is_task(text):
    return text.lstrip().startswith(task_indicator)


def is_project(text):
    return not is_task(text) and text.endswith(project_indicator)


def is_note(text):
    return not (is_task(text) or is_project(text))


# Tags

def _fix_tag(tag):
    if not tag.startswith(tag_indicator):
        tag = tag_indicator + tag
    return tag


def _create_tag_pattern(tag, include_suffix_space=False):
    tag = _fix_tag(tag)
    escaped_tag = re.escape(tag)
    pattern = r'(?:^|\s)' + escaped_tag + r'(\(([^)]*)\)(?:\s|$)|(?=\s)|$)'
    if include_suffix_space:
        pattern += '\s*'
    return re.compile(
        pattern
    )


def has_tag(text, tag):
    pattern = _create_tag_pattern(tag)
    return pattern.findall(text)


def get_tag_param(text, tag):
    pattern = _create_tag_pattern(tag)
    params = pattern.findall(text)
    if not params:
        return None
    param_with_parenthesis = params[0][0]
    pure_param = params[0][1]
    if not param_with_parenthesis:
        return None
    return pure_param


def remove_tag(text, tag):
    return replace_tag(text, tag, '')


def _prepare_param(param):
    if param is None:
        return ''
    else:
        return '({})'.format(param)


def _prepare_text_for_tag(text):
    if not text.endswith(' '):
        return text + ' '
    return text


def replace_tag(text, tag, replacement):
    pattern = _create_tag_pattern(tag, include_suffix_space=True)
    if replacement:
        replacement = ' ' + replacement + ' '
    else:
        replacement = ' '
    new_text = pattern.sub(replacement, text)
    if not text.endswith(' ') and new_text.endswith(' '):
        new_text = new_text.rstrip()
    return new_text


def add_tag(text, tag, param=None):
    param = _prepare_param(param)
    tag = _fix_tag(tag)
    full_tag = tag + param
    if not has_tag(text, tag):
        return _prepare_text_for_tag(text) + full_tag
    return replace_tag(text, tag, full_tag)


def enclose_tag(text, tag, prefix, suffix=None):
    suffix = suffix or prefix
    tag = _fix_tag(tag)
    param = _prepare_param(get_tag_param(text, tag))
    full_tag = tag + param
    replacement = prefix + full_tag + suffix
    return replace_tag(text, tag, replacement)


tag_pattern = tag_indicator + r'([^\s(]*)'


def get_all_tags(text, include_indicator=False):
    pattern = re.compile(tag_pattern)
    tags = pattern.findall(text)
    if include_indicator:
        return [tag_indicator + t for t in tags]
    return tags


def modify_tag_param(text, tag, modification):
    param = get_tag_param(text, tag)
    new_param = modification(param)
    return add_tag(text, tag, new_param)


def sort_by_tag_param(texts_collection, tag, reverse=False):
    def param_or_empty_text(t):
        param = get_tag_param(t, tag)
        return param if param else ''
    return tuple(sorted(
        texts_collection,
        key=param_or_empty_text,
        reverse=reverse
    ))


def toggle_tags(text, tags_with_params):
    """Args:
        tags_with_params (list of pairs): tag and it's param,
            param can be falsy or be strftime template
            in the last case datetime.now() is used to fill it
    """
    has_those_tags = [has_tag(text, tag) for tag, param in tags_with_params]
    if not any(has_those_tags):
        text = add_tag(text, *_toggle_tag_prep(tags_with_params[0]))
    elif has_those_tags[-1]:
        text = remove_tag(text, tags_with_params[-1][0])
    for i, (tag, has_this_tag) in enumerate(zip(tags_with_params[:-1], has_those_tags)):
        if has_this_tag:
            text = remove_tag(text, tag[0])
            text = add_tag(text, *_toggle_tag_prep(tags_with_params[i + 1]))
    return text


def _toggle_tag_prep(tag_param):
    tag, param = tag_param
    return tag, dt.datetime.now().strftime(param) if param else None


# Formatting

def strip_formatting(text):
    text = text.strip('\t')
    if is_task(text):
        return text[len(task_indicator):]
    elif is_project(text):
        return text[:-(len(project_indicator))]
    return text


def strip_formatting_and_tags(text):
    text = text.strip()
    if is_project(text):
        text = text[:-len(project_indicator)]
    if is_task(text):
        text = text[len(task_indicator):]
    for tag in get_all_tags(text):
        text = remove_tag(text, tag)
    return text.strip()


def calculate_indent_level(text):
    indentation_length = len(text) - len(text.lstrip('\t'))
    if indentation_length == 0:
        return 0
    indentation = text[:indentation_length]
    return len(indentation)


# Dates

def parse_datetime(text):
    try:
        return dt.datetime.strptime(text, '%Y-%m-%d %H:%M')
    except ValueError:
        return dt.datetime.strptime(text, '%Y-%m-%d')
