Django Robust Redirects
=======================

A more robust django redirect project.

Supports

- Regular expression redirects
- Ordinary direct redirects
- Partial path redirects


Installation
------------

1. Install the package from pip `pip install django-robust-redirects`
2. Add the following line to your INSTALLED_APPS::

```python
  INSTALLED_APPS = (
      ...
      'robustredirects'
  )
```

3. Add the following lines to your middleware::

```python
  MIDDLEWARE_CLASSES = (
      ...
      'robustredirects.middleware.RedirectMiddleware'
  )
```

4. Run syncdb to add the tables to your database


Converting from django.contrib.redirects
----------------------------------------

Robust redirects comes with a management command that will copy all django redirects over into robust redirects, just
run `python manage.py convert_redirects`