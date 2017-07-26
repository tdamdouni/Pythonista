# coding: utf-8


def parse_ref(bible_reference='1 John 5:3-5,7-10,14'):
    '''
    >>> parse_ref(' John ') == {'book': 'John'}
    True
    >>> parse_ref(' 1  John ') == {'book': '1 John'}
    True
    >>> parse_ref(' 1  John  3  ') == {'book': '1 John', 'chapter': 3}
    True
    >>> parse_ref(' 1  John  3  :  1 - 3 , 5, 7 - 9  ') == {
    ...     'book': '1 John', 'chapter': 3, 'verses': '1-3,5,7-9'}
    True
    '''
    book_and_chapter, _, verses = bible_reference.strip().partition(':')
    book, _, chapter = book_and_chapter.strip().rpartition(' ')
    try:  # see if the last word is an int
        chapter = int(chapter)
    except ValueError:  # if not then it is part of the book
        book = book_and_chapter
        chapter = 0     # and there is no chapter
    book = book.strip().replace(' ' * 3, ' ').replace(' ' * 2, ' ')
    book_chapter_and_verses = {'book': book}
    if chapter:
        book_chapter_and_verses['chapter'] = chapter
    verses = verses.replace(' ', '')
    if verses:
        book_chapter_and_verses['verses'] = verses
    return book_chapter_and_verses


def parse_refs(bible_reference):
    '''
    >>> refs = '1   John   5 : 3 - 5 , 7-10 , 14;Mark   7 : 4-6 ; 8 : 3 - 6,10'
    >>> parse_refs(refs) == [
    ...     {'book': '1 John', 'chapter': 5, 'verses': '3-5,7-10,14'},
    ...     {'book': 'Mark', 'chapter': 7, 'verses': '4-6'},
    ...     {'book': 'Mark', 'chapter': 8, 'verses': '3-6,10'}]
    True

    >>> parse_refs('Mark 1:1-4;5;8') == [
    ...     {'book': 'Mark', 'chapter': 1, 'verses': '1-4', },
    ...     {'book': 'Mark', 'chapter': 5},
    ...     {'book': 'Mark', 'chapter': 8}]
    True
    '''
    ref_list = []  # build up a list of dicts
    prev_book = ''
    for ref in bible_reference.split(';'):
        ref_dict = parse_ref(ref)
        if ref_dict['book']:              # if the ref includes a book
            prev_book = ref_dict['book']  # save that book for later
        else:                             # if ref does NOT include a book
            ref_dict['book'] = prev_book  # reuse the last book saved
        ref_list.append(ref_dict)
    return ref_list                       # return a list of dicts


refs = '1   John   5 : 3 - 5 , 7 - 10 , 14 ; Mark   7 : 4 - 6 ; 8 : 3 - 6 , 10'
if __name__ == '__main__':
    print(parse_refs(refs))
    print(parse_refs('Mark 1:1-4;5;8'))
