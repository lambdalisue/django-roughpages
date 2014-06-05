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
    Python 2.6, 2.7, 3.2, 3.3
Supported django versions
    Django 1.2 - 1.6

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
it prefer ``hoge_anonymous.html`` or ``hoge_authenticated.html`` than 
``hoge.html`` depends on the accessed user authentication state.
Thus you can simply prepare the page for authenticated user as
``<something>_authenticated.html`` and for anonymous user as
``<something>_anonymous.html``.

You can control the backend behavior with making a custom backend.
To make a custom backend, you need to inherit
``roughpages.backends.TemplateFilenameBackendBase`` and override
``prepare_filenames(self, filename, request)`` method.
The method receive an original filename and ``HttpRequest`` instance and
must return a filename list.
The django-roughpages then try to load template file from the beginning of
the list, thus the order of the appearance is the matter.

.. _flatpages: https://docs.djangoproject.com/en/dev/ref/contrib/flatpages/

Documentations
==============================================================================

.. toctree::
    :maxdepth: 2

    tutorials
    configurations
    backends

    API Reference <modules>


Indices and tables
-------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

