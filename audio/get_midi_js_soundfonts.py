#!/usr/bin/env python

'''
See: http://omz-forums.appspot.com/pythonista/post/5786871732895744
'''

import bs4, os, requests

base_url = 'https://github.com/gleitz/midi-js-soundfonts/tree/master/FluidR3_GM'

def get_instruments(url=base_url):
    print('Gathering midi-js-soundfonts from {}...'.format(url))
    soup = bs4.BeautifulSoup(requests.get(base_url).text)
    return [x.text for x in soup.find_all('a', href=True) if x.text.endswith('-mp3')]

def print_menu(instruments):
    print('{} midi-js-soundfonts were found.'.format(len(instruments)))
    print('\n'.join('{:>3} {}'.format(i, x) for i, x in enumerate(instruments)))

def get_mp3_from_filepath(filepath='acoustic_guitar_steel-mp3/A1.mp3'):
    fmt = '{}/{}?raw=true'
    url = fmt.format(base_url.replace('/tree/', '/blob/'), filepath)
    with open(filepath, 'wb') as out_file:
        out_file.write(requests.get(url).content)

def get_instrument_mp3s(instrument='acoustic_guitar_steel'):
    if not instrument.endswith('-mp3'):
        instrument += '-mp3'
    url = base_url + '/' + instrument
    print('Getting mp3 filenames for "{}" from "{}"...'.format(instrument, url))
    soup = bs4.BeautifulSoup(requests.get(url).text)
    filenames = [x.text for x in soup.find_all('a', href=True) if x.text.endswith('.mp3')]
    print('{} mp3 files were found.'.format(len(filenames)))
    if filenames:
        try:
            os.mkdir(instrument)
        except OSError:
            pass
    for i, filename in enumerate(filenames):
        filepath = instrument + '/' + filename
        print('Downloading file {:>2} of {}, {}...'.format(i+1, len(filenames), filepath))
        get_mp3_from_filepath(filepath)

def main():
    instruments = get_instruments(base_url)
    print_menu(instruments)
    try:
        fmt = 'Enter a number between 0 and {}: '
        i = int(raw_input(fmt.format(len(instruments)-1)) or 4)
    except ValueError:
        i = 4
    try:
        get_instrument_mp3s(instruments[i])
    except IndexError:
        sys.exit('User Error: {} is not a valid option!'.format(i))

if __name__ == '__main__':
    main()

# import bs4, requests
# url = 'https://github.com/gleitz/midi-js-soundfonts/tree/master/FluidR3_GM'
# soup = bs4.BeautifulSoup(requests.get(url).text)
# hrefs = [x for x in soup.find_all('a', href=True) if x.text.endswith('-mp3')]
# print('{} midi-js-soundfonts were found.'.format(len(hrefs)))
# print('\n'.join(x.text for x in hrefs))

# def get_mp3_from_filepath(filepath='acoustic_guitar_steel-mp3/A1.mp3'):
#    fmt = '{}/{}?raw=true'
#    url = fmt.format(base_url.replace('/tree/', '/blob/'), filepath)
#    with open(filepath, 'wb') as out_file:
#        out_file.write(requests.get(url).content)
