import clipboard
import Image
import photos

pic_para_menu_fmt = """
0 = no change ({})
1 = black/white
2 = grey
3 = RGB no transparency
4 = RGB with transparency
5 = CMYK
6 = YCbCr
7 = 32bit Pixel"""

pic_info_menu_fmt = """Picture-Information: resolution = {width} x {height} ({megapixels} MP), mode = {image_mode}

!!! Changing the resolution is time-consuming !!! Resolution higher 6000 x 4000 (24MP) can cause an abend!

0 = Auto processing (Resolution = {width} x {height}), quality = 95%, mode = {image_mode}
1 = Same resolution ({width} x {height})
2 = Define resolution
3 = 3MP (2048 x 1536)
5 = 5MP (2592 x 1936)"""

def pic_save(image, image_mode, width, height, quality, resize):
    print('\nPicture save is in process ...')
    if resize:
        image = image.resize((width, height), Image.ANTIALIAS)
    background = Image.new(image_mode, (width,height), 'white')
    background.paste(image, (0, 0))
    clipboard.set_image((background), format='jpeg', jpeg_quality=quality)
    photos.save_image(clipboard.get_image())
    fmt = 'Completed!\nResolution = {} x {}, quality = {:.0f}%, mode = {}'
    print(fmt.format(width, height, quality * 100, image_mode))

def pic_para(image_mode):
    quality = int(raw_input('\nQuality (0 - 100): ')) / 100.0
    if   quality < 0.0:
         quality = 0.0
    elif quality > 1.0:
         quality = 1.0
    print(pic_para_menu_fmt.format(image_mode))
    image_mode_old = image_mode
    image_mode = int(raw_input('Mode: '))
    menu_options = { 1 : '1',
                     2 : 'L',
                     3 : 'RGB',
                     4 : 'RGBA',
                     5 : 'CMYK',
                     6 : 'YCbCr',
                     7 : 'I' }
    return menu_options.get(image_mode, image_mode_old), quality

def main():
    if not photos.get_count():
        print('Sorry no access or no pictures.')
        return

    image2 = photos.pick_image()
    image = image2.convert('RGBA') #fix for current scene.load_pil_image()
    if not image:
        print('No image selected.  Good bye!')
        return

    resize = False
    quality = 95
    width, height = image.size
    megapixels = round(width * height / 1000000.0, 1)
    image_mode = image.mode
    print(pic_info_menu_fmt.format(**{ 'width'      : width,
                                       'height'     : height,
                                       'megapixels' : megapixels,
                                       'image_mode' : image_mode }))
    option = int(raw_input('Resolution: '))
    if option not in (0, 1, 2, 3, 5):
        print('Cancel: {} is not valid input.'.format(option))
        return

    if option == 0:
        quality /= 100.0
    elif option == 1:
        image_mode, quality = pic_para(image_mode)
    elif option == 2:
        print('\nChanging the ratio causes picture deformation!')
        width2 = int(raw_input('Width: '))
        ratio = width / (height * 1.0)
        suggestion = width2 / ratio
        height2 = int(raw_input('Height [Enter = {:.0f}]:'.format(suggestion)) or suggestion)
        if (width2 == width and height2 == height):
            resize = False
        else:
            resize = True
            width = width2
            height = height2
        image_mode, quality = pic_para(image_mode)
    elif option == 3:
        resolution3megapixel = (2048, 1536)
        resize = not (width in resolution3megapixel and height in resolution3megapixel)
        if resize:
            if width >= height:  # Landscape or Square
                width, height = resolution3megapixel  # Landscape
            else:
                height, width = resolution3megapixel  # Portrait
        image_mode, quality = pic_para(image_mode)
    elif option == 5:
        resolution5megapixel = (2592, 1936)
        resize = not (width in resolution5megapixel and height in resolution5megapixel)
        if resize:
            if width >= height:  # Landscape or Square
                width, height = resolution5megapixel  # Landscape
            else:
                height, width = resolution5megapixel  # Portrait
        image_mode, quality = pic_para(image_mode)
    pic_save(image, image_mode, width, height, quality, resize)

if __name__ == '__main__':
    main()
