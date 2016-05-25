"""zmqservice installation script

https://github.com/wagoodman/zmqservice
"""

#!/usr/bin/env python

import sys

from setuptools import setup


def read_long_description(readme_file):
    """ Read package long description from README file """
    try:
        import pypandoc
    except (ImportError, OSError) as exception:
        print('No pypandoc or pandoc: %s' % (exception,))
        if sys.version_info.major == 3:
            handle = open(readme_file, encoding='utf-8')
        else:
            handle = open(readme_file)
        long_description = handle.read()
        handle.close()
        return long_description
    else:
        return pypandoc.convert(readme_file, 'rst')

setup(
    name='zmqservice',
    version='0.1.0',
    packages=['zmqservice'],
    author='Tony Walker',
    url='https://github.com/wagoodman/zmqservice',
    license='MIT',
    description='zmqservice is a small Python library for '
                'writing lightweight networked services using zmq',
    long_description=read_long_description('README.md'),
    install_requires=[
        'msgpack-python',
        'pyzmq',
        'nose',
    ],
    #dependency_links=[
    #    'git+https://github.com/tonysimpson/nanomsg-python.git@master#egg=nanomsg',
    #],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
