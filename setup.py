#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="django-robust-redirects",
    version="1.0.1",
    url="http://github.com/spothero/django-robust-redirects",
    download_url="http://github.com/spothero/django-robust-redirects/tarball/0.10.0",
    description="A more robust and feature full django redirect package",
    author="SpotHero",
    author_email="pypi@spothero.com",
    packages=find_packages(exclude=['redirecttest*']),
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
    python_requires=">=3.6",
    install_requires=[
        "django>=3.2",
        "six>=1.12.0,<2"
    ],
)
