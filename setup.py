#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="django-robust-redirects",
    version="0.13.1",
    url="http://github.com/spothero/django-robust-redirects",
    download_url="http://github.com/spothero/django-robust-redirects/tarball/0.10.0",
    description="A more robust and feature full django redirect package",
    author="SpotHero",
    author_email="pypi@spothero.com",
    packages=["robustredirects"],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    install_requires=[
        "django>=1.10.3,<2",
        "future>=0.17.1,<1",
        "six>=1.12.0,<2"
    ],
)
