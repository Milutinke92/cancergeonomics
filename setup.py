from setuptools import setup

setup(
    name='Cancer Geonomics Client',
    version='0.1',
    py_modules=['cancergeonomics'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        cgccli=cancergeonomics.cli:cgccli
    ''',
)