# coding: utf-8

# https://gist.github.com/anonymous/ea1c8d3cf970eaaf517e

from _appex import finish, is_running_extension, get_input
import _appex

def _path2url(path):
    import urlparse
    import urllib
    return urlparse.urljoin('file:', urllib.pathname2url(path))

def get_attachments(uti='public.data'):
    output_attachments = []
    input_items = get_input()
    for item in input_items:
        attachments = item.get('attachments', None)
        if attachments:
            for attachment_dict in attachments:
                for attachment_type in attachment_dict:
                    if _appex._uti_conforms(attachment_type, uti):
                        output_attachments.append(attachment_dict[attachment_type])
    return output_attachments

def _image_from_attachment(image_attachment, image_type='pil', raw_data=False):
    image_type = image_type.lower()
    if not raw_data and image_type not in ['pil', 'ui']:
        raise TypeError('Unsupported image_type')
    
    use_ui = (image_type != 'pil')
    
    if isinstance(image_attachment, str):
        # raw image data
        if raw_data:
            return raw_data
        try:
            if use_ui:
                import ui
                return ui.Image.from_data(image_attachment)
            else:
                import Image
                from io import BytesIO
                buffer = BytesIO(image_attachment)
                img = Image.open(buffer)
                return img
        except:
            return None
    elif isinstance(image_attachment, unicode):
        # image path
        if raw_data:
            with open(image_attachment, 'r') as f:
                return f.read()
        try:
            if use_ui:
                import ui
                return ui.Image.named(image_attachment)
            else:
                import Image
                return Image.open(image_attachment)
        except:
            return None

def get_images(image_type='pil'):
    image_attachments = get_attachments('public.image')
    images = []
    if image_attachments:
        for image_attachment in image_attachments:
            img = _image_from_attachment(image_attachment, image_type)
            if img:
                images.append(img)
    return images

def get_image(image_type='pil'):
    image_attachments = get_attachments('public.image')
    if image_attachments:
        return _image_from_attachment(image_attachments[0], image_type)
    return None

def get_image_data():
    image_attachments = get_attachments('public.image')
    if image_attachments:
        return _image_from_attachment(image_attachments[0], raw_data=True)
    return None

def get_images_data():
    image_attachments = get_attachments('public.image')
    images = []
    if image_attachments:
        for image_attachment in image_attachments:
            data = _image_from_attachment(image_attachment, raw_data=True)
            if data:
                images.append(data)
    return images

def get_text():
    text_attachments = get_attachments('public.text')
    if text_attachments:
        return '\n'.join(text_attachments)
    return None

def get_urls():
    url_attachments = get_attachments('public.url')
    urls = []
    if url_attachments:
        for url_attachment in url_attachments:
            if url_attachment.startswith('/'):
                url = _path2url(url_attachment)
                urls.append(url)
            else:
                urls.append(url_attachment)
    return urls

def get_url():
    url_attachments = get_attachments('public.url')
    if url_attachments:
        url = url_attachments[0]
        if url.startswith('/'):
            return _path2url(url)
        return url
    return None

def get_file_paths():
    url_attachments = get_attachments('public.url')
    paths = []
    if url_attachments:
        for url_attachment in url_attachments:
            if url_attachment.startswith('/'):
                paths.append(url_attachment)
    return paths

def get_file_path():
    url_attachments = get_attachments('public.url')
    if url_attachments:
        first_path = url_attachments[0]
        if first_path.startswith('/'):
            return first_path
    text = get_text()
    if text and text.startswith('/') and os.path.exists(text):
        return text
    return None

def get_vcards():
    vcard_attachments = get_attachments('public.vcard')
    if vcard_attachments:
        return vcard_attachments
    return None

def get_vcard():
    vcard_attachments = get_attachments('public.vcard')
    if vcard_attachments:
        return vcard_attachments[0]
    return None
