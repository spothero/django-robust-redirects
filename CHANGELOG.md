# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0]
### Removed
- Errant `migrations` package

## [1.1.0]

### Changed 
- Now compatible with Django 4 

## [1.0.0]

### Removed
- Dropped support for all Python versions under Python 3.6.
- Dropped support for Django versions under Django 3.2.
- No longer using django-nose or nose test runner (ie django_nose.NoseTestSuiteRunner).

### Added
- Added AppConfig.

## [0.10.0]

### Added
- Add support for excluded URL path prefixes

### Changed
- Update for Django 1.9+

## [0.9.2]

### Added
- Require Django.

### Changed
- Fix typos in the help text.
- Prepend a slash when doing a partial replacement if the resulting url doesn’t have one. This avoid relative redirections.
- Fix the model admin form and use it in the admin.
