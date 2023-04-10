# Django Robust Redirects

A more robust django redirect project.

Supports

- Regular expression redirects
- Ordinary direct redirects
- Partial path redirects
- Excluding paths that will never be redirected


## Installation

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

4. Make and run migrations to add the tables to your database

5. (Optional) Add the following lines to your settings to ignore certain paths::

    ```python
      # URL path prefixes that should never be redirected
      ROBUST_REDIRECTS_IGNORED_PREFIXES = ('/api', '/admin')
    ```

## Converting from django.contrib.redirects

Robust redirects comes with a management command that will copy all django redirects over into robust redirects, just
run `python manage.py convert_redirects`

## Changelog

See the [CHANGELOG.md](CHANGELOG.md) file

## Running Tests
1. Change to the `redirecttest` directory
2. Install the requirements with `pip install -r requirements.txt`
3. Initialize the database with `python manage.py migrate`
4. Run the tests with `python manage.py test robustredirects`
