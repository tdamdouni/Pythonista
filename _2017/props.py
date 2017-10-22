#!python3

import photos
from objc_util import ObjCClass

CIImage = ObjCClass('CIImage')


def get_last_selfie():
    album = photos.get_selfies_album()
    assets = album.assets
    if assets:
        return assets[-1]  # PHAsset - https://developer.apple.com/documentation/photos/phasset?language=objc
    return None


def get_asset_data(asset):
    return asset.get_image_data().read()


def get_asset_properties(data):
    image = CIImage.imageWithData_(data)
    return image.properties()


def main():
    asset = get_last_selfie()
    if not asset:
        print('No asset')
        return

    data = get_asset_data(asset)
    properties = get_asset_properties(data)
    print(properties)


if __name__ == '__main__':
    main()