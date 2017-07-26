#!/usr/bin/env python
# coding: utf-8

import json, requests


def convert_dict_chapter(srce):
    '''return three dicts embedded inside each other: book, chapter, verse'''
    # print(json.dumps(srce, indent=4, sort_keys=True))
    return {srce['book_name']: {int(srce['chapter_nr']): {int(verse):
        verse_contents['verse'] for verse, verse_contents
            in srce['chapter'].iteritems()}}}


def convert_dict(srce):
    '''return three dicts embedded inside each other: book, chapter, verse'''
    # print(json.dumps(srce, indent=4, sort_keys=True))
    if srce['type'] == 'chapter':
        return convert_dict_chapter(srce)
    elif srce['type'] == 'verse':
        return convert_dict_chapter(srce['book'][0])
    return {srce['book_name']: {int(chapter): {int(verse): verse_contents['verse']
            for verse, verse_contents in chapter_contents['chapter'].iteritems()}
                for chapter, chapter_contents in srce['book'].iteritems()}}


def passage_as_dict(ref, version='nasb'):
    '''getbible.net does not valid json so we convert (content); to [content]'''
    fmt = 'https://getbible.net/json?p={}&v={}'
    url = fmt.format(ref.strip().replace(' ', '%20'), version.strip())
    return convert_dict(json.loads(requests.get(url).text[1:-2]))


def passages_as_dicts(ref, version='nasb'):
    return [passage_as_dict(p, version) for p in ref.split(';') if p.strip()]


# Matthew is 'type': 'book', Mark is 'chapter', Luke and John are 'verse'
passages = passages_as_dicts('Matthew;Mark 2;Luke 2:1;John 2:8-12')
print(json.dumps(passages, indent=4, sort_keys=True))
