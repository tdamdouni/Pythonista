import os
import shutil
import errno


APPDIR = 'apps'


ACCESS_TOKEN_NAME = 'DropboxAccesstoken.token'
DEFAULT_APP_NAME = 'dmmmd sync'
PYTHON_CONSTANTS = 'constants.py'
CONSTANTS_MODULE = PYTHON_CONSTANTS.strip(".py")


def get_constants(app_name=DEFAULT_APP_NAME):
    """return constants for filenames for each app"""
    app_name_underscore = app_name.replace(' ', '_')
    access_token_name_underscore = '_'.join(
        (app_name_underscore, ACCESS_TOKEN_NAME))
    if has_app_dir() is True:
        token_filename = os.path.join(
            APPDIR, app_name_underscore, ACCESS_TOKEN_NAME)
    else:
        token_filename = access_token_name_underscore
    return app_name_underscore, token_filename


def make_apps_dir():
    if has_app_dir() is False:
        os.mkdir(APPDIR)
        return True


def is_iOS_platform():
    """attrs on iOS platform, returns True if all are True, values
    take from an iPad"""
    import platform

    iOS_attrs = [
        os.name == 'posix',
        platform.system().lower() == "darwin",
        int(platform.release().split('.')[0]) == 14,
    ]
    return all(iOS_attrs)


def has_app_dir():
    if os.path.exists(APPDIR) is True:
        return True
    else:
        return False


def get_app_filenames():
    """returns a tuple of app filenames to be copied and
    flat_filenames for new files in project directory"""
    if is_iOS_platform() is False:
        exclude = ('.', '__')
        include = ('.token', '.py')
        valid_names = ('Dropbox', 'constants')
        app_filenames = []
        flat_filenames = []
        for root, directories, files in os.walk(APPDIR):
            files = [app_file for app_file in files
                     if all([not any([app_file.startswith(item)
                            for item in exclude]),
                            any([app_file.endswith(item)
                                for item in include]),
                            any(item in app_file
                                for item in valid_names)])]
            if len(files) > 0:
                basename = os.path.basename(root)
                app_filenames.extend([os.path.join(root, filename)
                                      for filename in files])
                flat_filenames.extend([os.path.join(
                    root, '_'.join((basename, filename)))
                    for filename in files])
        return app_filenames, flat_filenames
    else:
        message = "This function only valid on a non-iOS platform"
        raise ValueError(message)


def copy_iOS_app_files_on_non_iOS():
    app_filenames, flat_filenames = get_app_filenames()
    for app_filename, flat_filename in zip(app_filenames, flat_filenames):
        try:
            shutil.copy(app_filename, flat_filename)
        except IOError as e:
            if e.errno == errno.EACCES:  # read only file
                os.remove(flat_filename)
                shutil.copy(app_filename, flat_filename)


def remove_iOS_app_files():
    """removes all the app files from project directory,
    in pythonista that is the home directory"""
    _, flat_filenames = get_app_filenames()
    for flat_filename in flat_filenames:
        if os.path.exists(flat_filename):
            os.remove(flat_filename)
