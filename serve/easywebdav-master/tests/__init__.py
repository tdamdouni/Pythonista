import os
import unittest
import atexit
import subprocess
import inspect
import requests
import time
import shutil
import tempfile
from functools import partial

import easywebdav

SERVER_USERNAME = 'testuser'
SERVER_PASSWORD = SERVER_USERNAME
SERVER_PORT = 28080
SERVER_URL = 'http://localhost:{}'.format(SERVER_PORT)

_initialized = False
_init_failed = False
_server_process = None
_server_path = None
_client = None
def init():
    global _initialized, _init_failed, _server_process, _server_path, _client
    if _init_failed:
        raise unittest.SkipTest('Test session initialization failed')
    try:
        if _initialized:
            return

        # Create server
        output('Starting WebDAV server')
        _server_path = '/tmp/easywebdav_tests'#tempfile.mkdtemp()
        if os.path.exists(_server_path):
            shutil.rmtree(_server_path)
        os.makedirs(_server_path)
        process_props = dict(
            args='davserver -D {path} -u {username} -p {password} -P {port}'.format(
                path=_server_path,
                username=SERVER_USERNAME,
                password=SERVER_PASSWORD,
                port=SERVER_PORT,
                ),
            shell=True,
            )
        if "WEBDAV_LOGS" not in os.environ:
            process_props.update(
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                )
        _server_process = subprocess.Popen(**process_props)
        atexit.register(terminate_server)

        # Ensure server is running
        ensure_server_initialized()

        # Create client
        _client = easywebdav.connect(
            host='localhost',
            port=SERVER_PORT,
            username=SERVER_USERNAME,
            password=SERVER_PASSWORD,
            )

        _initialized = True
    except:
        _init_failed = True
        raise

def ensure_server_initialized():
    output('Waiting for WebDAV server to start up...')
    timeout = time.time() + 20
    while True:
        if time.time() >= timeout:
            raise Exception('WebDAV server did not respond within the expected time frame')
        try:
            response = requests.head(SERVER_URL, auth=(SERVER_USERNAME, SERVER_PASSWORD))
        except requests.RequestException:
            continue
        if response.status_code < 300:
            break
        time.sleep(0.5)
    output('WebDAV server startup complete')

def terminate_server():
    output('Shutting down WebDAV server...')
    _server_process.terminate()
    _server_process.communicate()
    output('WebDAV server shutdown complete')
    shutil.rmtree(_server_path)

def output(msg, *args, **kwargs):
    if args or kwargs:
        msg = msg.format(args, kwargs)
    print(msg)

class TestCase(unittest.TestCase):
    def setUp(self):
        init()
        self.client = ClientProxy(self, _client)
        self.client.cd('/')
    def tearDown(self):
        self._reset()
    def _reset(self, dir=None):
        dir = dir or _server_path
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isdir(path):
                self._reset(path)
                os.rmdir(path)
                continue
            os.remove(path)
    def _path(self, path):
        return os.path.join(_server_path, path)
    def _create_dir(self, *paths):
        for p in paths:
            os.makedirs(self._path(p))
    def _list_dir(self, path):
        return os.listdir(self._path(path))
    def _create_file(self, path, contents='Dummy content\n'):
        with open(self._path(path), 'w') as f:
            f.write(contents)
    def _read_file(self, path):
        with open(self._path(path)) as f:
            return f.read()
    def _assert_dir(self, path):
        path = self._path(path.lstrip('/'))
        assert os.path.isdir(path), 'Expected directory does not exist: ' + path
    def _assert_file(self, path, contents=None):
        path = self._path(path)
        assert os.path.isfile(path), 'Expected file does not exist: ' + path
        if contents:
            self._assert_local_file(path, contents)
    def _assert_local_file(self, absolute_path, contents=None):
        with open(absolute_path) as f:
            self.assertEqual(contents, f.read())
    def _assert_doesnt_exist(self, path):
        assert not os.path.exists(self._path(path)), 'Path should not have existed, but exists: ' + path
    def _local_file(self, contents='Dummy content\n'):
        ''' Create a temporary local file and return its path. The file will be
        deleted at the end of the test. '''
        handle, path = tempfile.mkstemp()
        if contents is not None:
            with open(path, 'w') as f:
                f.write(contents)
        self.addCleanup(partial(os.close, handle))
        return path
    def _local_path(self):
        ''' Get a temporary non-existent path. '''
        handle, path = tempfile.mkstemp()
        os.close(handle)
        os.remove(path)
        return path

class ClientProxy(object):
    def __init__(self, test, client):
        self.__test__ = test
        self.__client__ = client
    def __getattr__(self, attr):
        value = getattr(self.__client__, attr)
        if attr != 'cd' and inspect.isroutine(value):
            return MethodProxy(self.__test__, self.__client__, value)
        return value

class MethodProxy(object):
    def __init__(self, test, client, method):
        self.__test__ = test
        self.__client__ = client
        self.__method__ = method
    def __call__(self, *args, **kwargs):
        cwd_before = self.__client__.cwd
        result = self.__method__(*args, **kwargs)
        cwd_after = self.__client__.cwd
        self.__test__.assertEqual(cwd_before, cwd_after,
            'CWD has changed during method "{}":\n  Before: {}\n  After:  {}'
            .format(self.__method__.__name__, cwd_before, cwd_after))
        return result
