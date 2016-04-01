import os

from setuptools import setup, find_packages


classifiers = """\
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Topic :: Internet :: File Transfer Protocol (FTP)
Operating System :: Unix
"""

def read(*rel_names):
    return open(os.path.join(os.path.dirname(__file__), *rel_names)).read()


setup(
    name='sftpserver',
    version='0.2',
    url='http://github.com/rspivak/sftpserver',
    license='MIT',
    description='sftpserver - a simple single-threaded sftp server',
    author='Ruslan Spivak',
    author_email='ruslan.spivak@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['distribute', 'paramiko'],
    zip_safe=False,
    entry_points="""\
    [console_scripts]
    sftpserver = sftpserver:main
    """,
    classifiers=filter(None, classifiers.split('\n')),
    long_description=read('README.rst'),
    extras_require={'test': []}
    )
