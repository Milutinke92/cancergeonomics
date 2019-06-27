import os

from setuptools import setup

VERSION_FILE = 'VERSION'
version = '0.1+local'
if os.path.isfile(VERSION_FILE):
    with open(VERSION_FILE, 'r') as f:
        version = f.read()

install_requires = ['Click==7.0', 'requests==2.22']

setup(
    name='cancergeonomics',
    version=version,
    py_modules=['cancergeonomics'],
    install_requires=install_requires,
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    platforms=['Windows', 'POSIX', 'MacOS'],
    maintainer='Stefan Milutinovic',
    maintainer_email='stefan@milutinovic.com',
    url='https://github.com/sbg/sevenbridges-python',
    entry_points='''
        [console_scripts]
        cgccli=cancergeonomics.cli:cgccli
    ''',
)
