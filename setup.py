#!/usr/bin/env python

import embedded_media as emb

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='django-embedded-media',
    version=emb.__version__,
    description=emb.__description__,
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    keywords='django media',
    maintainer='Derek Payton',
    maintainer_email='derek.payton@gmail.com',
    url='https://github.com/dmpayton/django-embedded-media',
    download_url='https://github.com/dmpayton/django-embedded-media/tarball/v%s' % emb.__version__,
    license=emb.__license__,
    include_package_data=True,
    packages=find_packages(exclude=('tests',)),
    test_suite='tests.setuptest.SetupTestSuite',
    tests_require=(
        'coverage',
        'django>=1.4',
        'pep8',
      ),
    zip_safe=False,
    )
