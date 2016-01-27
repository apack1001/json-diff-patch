#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst')
except:
    description = ''


setup(
    name='json_diff_patch',
    version='0.5.0',

    packages=['json_diff_patch'],
    package_dir={'json_diff_patch': 'lib'},
    install_requires=['colorama'],

    entry_points={
        'console_scripts': [
            'json = json_diff_patch.__main__:main',
        ]
    },

    author='apack1001',
    author_email='apack1001@gmail.com',
    url='https://github.com/apack1001/json-diff-patch',

    description='A set of tools to manipulate JSON: diff, patch, pretty-printing',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License'
    ],

    keywords=['json'],

    long_description=description
)
