# https://forum.omz-software.com/topic/3961/extract-a-tar-gz-file

import tarfile
with tarfile.open("sample.tar.gz") as tarball:
	tarball.extractall()

