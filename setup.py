#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os

setup(
    name = "django-robust-redirect",
    version = "0.9",
    url = 'http://github.com/spothero/django-robust-redirect',
    download_url = 'http://github.com/spothero/django-robust-redirect/tarball/0.9',
    description = "A more robust and featurefull django redirect package",
    author = 'SpotHero and Glen Zangirolami',
    author_email = 'cezar@spothero.com',
    packages = ['redirect'],
    include_package_data = True,
    zip_safe = False,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
