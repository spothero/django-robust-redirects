#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="django-robust-redirects",
    version="0.9.2",
    url='http://github.com/spothero/django-robust-redirects',
    download_url='http://github.com/spothero/django-robust-redirects/tarball/0.9.2',
    description="A more robust and feature full django redirect package",
    author='SpotHero and Glen Zangirolami',
    author_email='cezar@spothero.com',
    packages=['robustredirects'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ], requires=['django']
)
