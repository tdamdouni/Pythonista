# -*- coding: utf-8 -*-
import os
import pprint
try:
    from dropbox_client import get_client
except:
    from site_packages.dropbox_client import get_client

pp = pprint.PrettyPrinter(indent=4)
APP_NAME = 'dmmmd sync'
OVERWRITE = True
NEWFILE = True
client = get_client(APP_NAME)


def dropbox_file_and_metadata(filepath):
    """returns a filelike object from filepath in dropbox"""
    result = client.get_file_and_metadata(filepath)
    return result


def dropbox_files_and_metadata(download_filepaths):
    """returns a list of tuples of (dropbox file object, metadata)"""
    return [dropbox_file_and_metadata(filepath)
            for filepath in download_filepaths]


class Metadata(object):
    """return an object with attrs"""
    local_root = 'pythonista'

    def __init__(self, dropbox_metadata):
        # update Metadata attrs with dropbox metadata dict
        self.__dict__.update(dropbox_metadata)
        # pythonista on iOS cannot have directories, set root to curdir '.'
        if file_exists(self.local_root) is False:
            self.local_root = os.curdir
        self.basename = os.path.basename(self.path)

    def destination_filename(self):
        """docstring for destination_filename"""
        return os.path.join(self.local_root, self.basename)


class PackageMetadata(Metadata):
    package_root = 'site-packages'

    def destination_filename(self):
        """docstring for destination_filename"""
        return os.path.join(self.local_root, self.package_root, self.basename)


def save_files_to_pythonista(download_filepaths, meta_data):
    files_and_metadata = dropbox_files_and_metadata(download_filepaths)
    files_and_metadata = convert_files_and_metadata(
        files_and_metadata, meta_data)
    write_downloaded_files(files_and_metadata)


def write_downloaded_files(files_and_metadata):
    for dropbox_file, metadata in files_and_metadata:
        destination_filename = metadata.destination_filename()
        overwrite = NEWFILE
        if file_exists(destination_filename) is True:
            overwrite, message = get_overwrite_state(destination_filename)
            if overwrite == 'n':
                print message
        if any([overwrite == NEWFILE, overwrite == 'y']):
            message = "Downloading file '{filename}' from Dropbox.".\
                format(filename=metadata.path)
            with open(destination_filename, 'w') as fh:
                print message
                fh.write(dropbox_file.read())


def get_overwrite_state(filename):
    """ask user if existing file should be overwritten"""
    overwrite = NEWFILE
    message = "Overwrite the existing file '{filename}'?[y/n]".\
        format(filename=filename)
    while overwrite is NEWFILE:
        overwrite = raw_input(message).strip()
    if overwrite == 'n':
        message = "The file '{filename}' will not be overwritten.".\
            format(filename=filename)
    return overwrite, message


def convert_files_and_metadata(files_and_metadata, meta_data):
    # convert dropbox metadata dicts into an object with filepath attrs
    files_and_metadata = [(dropbox_file, meta_data(metadata))
                          for dropbox_file, metadata
                          in files_and_metadata]
    return files_and_metadata


def file_exists(filename):
    return os.path.exists(filename)


def test_modules():
    download_package_paths = [
        'Neville_Shared/projects/dev/python/csv_munging/numbers_spreadsheet.py',
    ]
    save_files_to_pythonista(download_package_paths, PackageMetadata)
    assert file_exists(
        './pythonista/site-packages/numbers_spreadsheet.py') is True


def test_files():
    download_filepaths = [
        'notesy/foo.txt',
    ]
    save_files_to_pythonista(download_filepaths, Metadata)
    assert os.path.exists(
        './pythonista/foo.txt') is True


if __name__ == '__main__':
    test_files()
    test_modules()
