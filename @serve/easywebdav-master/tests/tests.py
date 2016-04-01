import platform

python_version, _, __ = platform.python_version_tuple()
if python_version == '2':
    from StringIO import StringIO
else:
    from io import StringIO

from . import TestCase

class Tests(TestCase):
    content = '123\n123\n'

    def test__cd_cwd(self):
        self._create_dir('one')
        self.client.cd('one')
        self.assertEqual('/one/', self.client.cwd)
    def test__cd_cwd_absolute(self):
        self._create_dir('one', 'two/three')
        self.client.cd('one')
        self.assertEqual('/one/', self.client.cwd)
        self.client.cd('/two/three')
        self.assertEqual('/two/three/', self.client.cwd)

    def test__exists(self):
        self._create_dir('one/two', 'three/four')
        self.assertTrue(self.client.exists('one'))
        self.assertFalse(self.client.exists('two'))
        self.assertTrue(self.client.exists('three'))
        self.assertFalse(self.client.exists('four'))
        self.assertTrue(self.client.exists('one/two'))
        self.client.cd('one')
        self.assertFalse(self.client.exists('one'))
        self.assertTrue(self.client.exists('two'))
        self.assertTrue(self.client.exists('/three'))
        self.assertTrue(self.client.exists('/three/four'))

    def test__create_dir(self):
        self.client.mkdir('one')
        self._assert_dir('one')
    def test__create_nested_dir(self):
        self.client.mkdir('one')
        self.client.mkdir('one/two')
        self._assert_dir('one/two')
    def test__create_dir_in_nested_cwd(self):
        self.client.mkdir('one')
        self.client.cd('one')
        self.client.mkdir('two')
        self._assert_dir('one/two')
    def test__create_multiple_nested_dirs(self):
        self.client.mkdirs('one/two')
        self._assert_dir('one/two')
    def test__create_absolute_dir(self):
        self.client.mkdir('one')
        self.client.cd('one')
        self.client.mkdir('/two')
        self._assert_dir('two')
        self._assert_doesnt_exist('one/two')
    def test__create_absolute_dir_in_nested_cwd(self):
        self.client.mkdir('one')
        self.client.cd('one')
        self.client.mkdir('/one/two')
        self._assert_dir('one/two')
        self.client.mkdir('/three')
        self.client.mkdir('/three/four')
        self._assert_dir('three/four')
        self._assert_doesnt_exist('one/three')
    def test__create_multiple_absolute_nested_dirs(self):
        self.client.mkdir('one')
        self.client.cd('one')
        self.client.mkdirs('/two/three')
        self._assert_doesnt_exist('one/two')
        self._assert_dir('two/three')

    def test__delete_dir(self):
        self._create_dir('one')
        self.client.rmdir('one')
        self._assert_doesnt_exist('one')
    def test__delete_nested_dir(self):
        self._create_dir('one/two')
        self.client.rmdir('one/two')
        self._assert_dir('one')
        self._assert_doesnt_exist('one/two')
    def test__delete_dir_absolute(self):
        self._create_dir('one', 'two/three')
        self.client.cd('one')
        self.client.rmdir('/two/three')
        self._assert_dir('two')
        self._assert_doesnt_exist('two/three')

    def test__delete_file(self):
        self._create_file('one')
        self.client.delete('one')
        self._assert_doesnt_exist('one')
    def test__delete_nested_file(self):
        self._create_dir('one')
        self._create_file('one/two')
        self.client.delete('one/two')
        self._assert_dir('one')
        self._assert_doesnt_exist('one/two')
    def test__delete_file_absolute(self):
        self._create_dir('one', 'two')
        self._create_file('two/three')
        self.client.cd('one')
        self.client.delete('/two/three')
        self._assert_dir('two')
        self._assert_doesnt_exist('three')

    def test__download(self):
        self._create_file('file', self.content)
        path = self._local_path()
        self.client.download('file', path)
        self._assert_local_file(path, self.content)
    def test__download_nested(self):
        self._create_dir('one')
        self._create_file('one/file', self.content)
        path = self._local_path()
        self.client.download('one/file', path)
        self._assert_local_file(path, self.content)
    def test__download_absolute(self):
        self._create_dir('one', 'two')
        self._create_file('two/file', self.content)
        path = self._local_path()
        self.client.cd('one')
        self.client.download('/two/file', path)
        self._assert_local_file(path, self.content)
    def test__download_stream(self):
        self._create_file('file', self.content)
        sio = StringIO()
        self.client.download('file', sio)
        self.assertEqual(self.content, sio.getvalue())

    def test__upload(self):
        path = self._local_file(self.content)
        self.client.upload(path, 'file')
        self._assert_file('file', self.content)
    def test__upload_nested(self):
        path = self._local_file(self.content)
        self._create_dir('one')
        self.client.upload(path, 'one/file')
        self._assert_file('one/file', self.content)
    def test__upload_nested_absolute(self):
        path = self._local_file(self.content)
        self._create_dir('one', 'two')
        self.client.cd('one')
        self.client.upload(path, '/two/file')
        self._assert_file('two/file', self.content)
    def test__upload_stream(self):
        sio = StringIO()
        sio.write(self.content)
        sio.seek(0)
        self.client.upload(sio, 'file')
        self._assert_file('file', self.content)
