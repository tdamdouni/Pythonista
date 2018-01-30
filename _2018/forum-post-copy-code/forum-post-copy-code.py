#!python3

import requests
import urllib3
import json
import re
import clipboard
import appex

CODE_PATTERN = re.compile('\<code.*?\>(.*?)\<\/code\>', re.MULTILINE | re.DOTALL)


def get_code_elements(url):
    parsed = urllib3.util.parse_url(url)

    if not parsed.host == 'forum.omz-software.com':
        raise ValueError(f'{url} does not point to the Pythonista Forum')

    path = parsed.path
    if not path.startswith('/api/'):
        path = f'/api{path}'

    url = f'{parsed.scheme}://{parsed.host}{path}'

    j = json.loads(requests.get(url).text)

    try:
        post = int(url.split('/')[-1])
        content = j['posts'][post-1]['content']
        return re.findall(CODE_PATTERN, content)
    except ValueError as e:
        raise ValueError('You have to select specific post from topic, ie. URL should end with /NUMBER') from e


def main():
    if appex.is_running_extension():
        url = appex.get_url() or appex.get_text()
    else:
        import console

        try:
            url = console.input_alert('Enter URL').strip()
            if not url:
                return
        except KeyboardInterrupt:
            return

    print(f'Searching for <code> elements at {url}')
    try:
        elements = get_code_elements(url)

        if not elements:
            print(f'No <code> elements found')
            return

        result = '\n\n'.join([
            f'# <code> element no {idx+1}\n\n' + code
            for idx, code in enumerate(elements)
        ])

        clipboard.set(result)
        print(result)
        print(f'{len(elements)} <code> element(s) copied to the clipboard')

    except Exception as e:
        print(f'Failed to get <code> element values: {e}')


if __name__ == '__main__':
    main()