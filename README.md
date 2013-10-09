Django Robust Redirects
=======================

A more robust django redirect project.

Supports

- Regular expression redirects
- Partial path redirects


Installation
------------

1. Install the package from pip `pip install django-robust-redirects`
2. Add the following line to your INSTALLED_APPS::

  INSTALLED_APPS = (
      ...
      'redirect'
  )

4. Add the following lines to your middleware::

  MIDDLEWARE_CLASSES = (
      ...
      'redirect.middleware.RedirectMiddleware'
  )
