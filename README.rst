django-roughpages
==========================
.. image:: https://secure.travis-ci.org/lambdalisue/django-roughpages.png?branch=master
    :target: http://travis-ci.org/lambdalisue/django-roughpages
    :alt: Build status

.. image:: https://coveralls.io/repos/lambdalisue/django-roughpages/badge.png?branch=master
    :target: https://coveralls.io/r/lambdalisue/django-roughpages/
    :alt: Coverage

.. image:: https://pypip.in/d/django-roughpages/badge.png
    :target: https://pypi.python.org/pypi/django-roughpages/
    :alt: Downloads

.. image:: https://pypip.in/v/django-roughpages/badge.png
    :target: https://pypi.python.org/pypi/django-roughpages/
    :alt: Latest version

.. image:: https://pypip.in/wheel/django-roughpages/badge.png
    :target: https://pypi.python.org/pypi/django-roughpages/
    :alt: Wheel Status

.. image:: https://pypip.in/egg/django-roughpages/badge.png
    :target: https://pypi.python.org/pypi/django-roughpages/
    :alt: Egg Status

.. image:: https://pypip.in/license/django-roughpages/badge.png
    :target: https://pypi.python.org/pypi/django-roughpages/
    :alt: License

Author
    Alisue <lambdalisue@hashnote.net>
Supported python versions
    Python 2.7, 3.3, 3.4, 3.5
Supported django versions
    Django 1.7 - 1.10

An template based the flatpages_ like app.
Not like django's flatpages app, django-roughpages render a template file which
determined from the accessed URL.
It is quite combinient when you want to render simple static page.
You do not need to prepare ``urls.py`` or ``views.py`` anymore for that kind
of simple static page.

django-roughpages call ``roughpages.views.roughpage`` view with the accessed
URL when django raise ``Http404`` exception.
The view automatically find the corresponding template file from ``roughpages``
directory in one of your template directories.
Assume if the user accessed http://localhost/foo/bar/hoge/.
If there is no urls pattern patched with the URL, django-roughpages try to find
corresponding template file such as ``templates/roughpages/foo/bar/hoge.html``.
If django-roughpages find the corresponding template file, it will render the
template and return the ``HttpResponse``, otherwise it re-raise ``Http404``
exception.

You can complicatedly select the corresponding template file.
django-roughpages determine the filename with a backend system.
The default backend is ``roughpages.backends.AuthTemplateFilenameBackend`` and
it prefer ``hoge.anonymous.html`` or ``hoge.authenticated.html`` than 
``hoge.html`` depends on the accessed user authentication state.
Thus you can simply prepare the page for authenticated user as
``<something>.authenticated.html`` and for anonymous user as
``<something>.anonymous.html``.
Note that the filename which contains ``'.'`` is not allowed thus user cannot 
access ``hoge.authenticated.html`` with a url like ``/hoge.authenticated`` to prevent unwilling file acccess.

You can control the backend behavior with making a custom backend.
To make a custom backend, you need to inherit
``roughpages.backends.TemplateFilenameBackendBase`` and override
``prepare_filenames(self, filename, request)`` method.
The method receive an original filename and ``HttpRequest`` instance and
must return a filename list.
The django-roughpages then try to load template file from the beginning of
the list, thus the order of the appearance is the matter.

.. _flatpages: https://docs.djangoproject.com/en/dev/ref/contrib/flatpages/

Documentation
-------------
http://django-roughpages.readthedocs.org/en/latest/

Installation
------------
Use pip_ like::

    $ pip install django-roughpages

.. _pip:  https://pypi.python.org/pypi/pip

Usage
-----

Configuration
~~~~~~~~~~~~~
1.  Add ``roughpages`` to the ``INSTALLED_APPS`` in your settings
    module

    .. code:: python

        INSTALLED_APPS = (
            # ...
            'roughpages',
        )

2.  Add our extra fallback middleware

    .. code:: python

        MIDDLEWARE_CLASSES = (
            # ...
            'roughpages.middleware.RoughpageFallbackMiddleware',
        )

3.  Create ``roughpages`` directory in one of your template directories
    specified with ``settings.TEMPLATE_DIRS``


Quick tutorial
~~~~~~~~~~~~~~~
1.  Create ``roughpages/foo/bar/hoge.html`` as follow

    .. code:: html

        <html>
        <body>
            This is Hoge
        </body>
        </html>

2.  Run syncdb and Start development server with
    ``python manage.py syncdb; python manage.py runserver 8000``

3.  Access http://localhost:8000/foo/bar/hoge/ and you will see "This is Hoge"

4.  Create ``roughpages/foo/bar/piyo.anonymous.html`` as follow

    .. code:: html

        <html>
        <body>
            This is Piyo Anonymous
        </body>
        </html>

5.  Create ``roughpages/foo/bar/piyo.authenticated.html`` as follow

    .. code:: html

        <html>
        <body>
            This is Piyo Authenticated
        </body>
        </html>

6.  Access http://localhost:8000/foo/bar/piyo/ and you will see
    "This is Piyo Anonymous"

7.  Access http://localhost:8000/admin/ and login as admin user.

8.  Access http://localhost:8000/foo/bar/piyo/ and you will see
    "This is Piyo Authenticated"


.. Note::
    
    Any dots ('.') in a last part of URL is replaced to underscore ('_') to prevent a security risk.
    See https://github.com/lambdalisue/django-roughpages/issues/3
