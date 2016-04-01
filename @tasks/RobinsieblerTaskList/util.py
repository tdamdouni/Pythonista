#------------------------------------------
# Name:     util
# Purpose:  Utility functions for other scripts
#
# Author:   Robin Siebler
# Created:  7/17/13
#------------------------------------------
__author__ = 'Robin Siebler'
__date__ = '7/17/13'

import os, pickle

FILE_EXT = '.tsk'  # save, load, and delete only files with this suffix

def valid_filename(filename):
    if not filename:
        return filename
    return filename if filename.endswith(FILE_EXT) else filename + FILE_EXT

def validate_file(filename):
    """Verify that the specified file exists.

    :param task_file: The file name provided by the user.
    """

    filename = valid_filename(filename)
    return filename if filename and os.path.exists(filename) else None

def handle_error(filename):
    print('ERROR: "{}" is not a valid task file.'.format(filename))

def delete(filename):
    """Delete the task file specified by the user.

    :param task_file: a previously created task file
    """

    new_name = validate_file(filename)
    if new_name:
        os.remove(new_name)
    else:
        handle_error(filename)

def load(filename):
    """Loads a file that has been pickled and reads its contents.

    :param pickle_file: the file that has been pickled
    :return: The object in the file, or None if an error occurs
    """

    new_name = validate_file(filename)
    if new_name:
        try:
            with open(new_name, 'rb') as fh:
                return pickle.load(fh)
        except (IOError, pickle.PickleError) as e:
            print(e)
            return None
    else:
        handle_error(filename)

def save(obj, filename):
    """Save an object into a pickle file.

    :param obj: The object to pickle
    :param pickle_file: The name of the file to create.
    """

    filename = valid_filename(filename)
    if filename:
        try:
            with open(filename, 'wb') as fh:
                pickle.dump(obj, fh)
        except (IOError, pickle.PickleError) as e:
            print(e)
    else:
        handle_error(filename)

def tests():
    print('-' * 20 +'\nTest run starts...')
    test_payload = 'Will this really work?!?'
    test_file = 'delete me'
    test_file_with_ext = test_file + FILE_EXT
    for filename in (test_file_with_ext, test_file):
        print('  Testing: ' + filename)
        assert valid_filename(filename) == test_file_with_ext
        assert not os.path.exists(filename)
        assert not validate_file(filename)
        print('Loading a nonexisting file should print an error...')
        load(filename)
        print('Deleting a nonexisting file should print an error...')
        delete(filename)
        # create file...
        save(test_payload, filename)
        assert os.path.exists(test_file_with_ext)
        assert validate_file(filename)
        assert load(filename) == test_payload
        assert os.path.exists(test_file_with_ext)
        assert validate_file(filename)
        delete(filename)
        assert not os.path.exists(test_file_with_ext)
        assert not validate_file(filename)
    for filename in ('', None, 0):  # , ['hi']):
        print('  Testing: {}: Should print 3 errors...'.format(filename))
        save(test_payload, filename)
        load(filename)
        delete(filename)
    print('Test run complete.')

if __name__ == '__main__':
    tests()
    #pass  # put call to unit tests here?
