# https://github.com/cclauss/Ten-lines-or-less/blob/master/appex_dump.py

# coding: utf-8

# See: https://forum.omz-software.com/topic/2358/appex-safari-content

import appex

def main():
    if appex.is_running_extension():
        for func in (appex.get_attachments, appex.get_file_path,
            appex.get_file_paths, appex.get_image, appex.get_images,
            appex.get_text, appex.get_url, appex.get_urls,
            appex.get_vcard, appex.get_vcards):
            print('{:<11} : {}'.format(func.func_name.partition('_')[2], func()))

if __name__ == '__main__':
    main()