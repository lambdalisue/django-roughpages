Tutorials
============
django-roughpages have several distincitive features to help you to make static
pages.
You should follow at least the "Quick tutorial" section to get the image of
django-roughpages.


Quick tutorial
---------------
If you have not installed django-roughpages yet, you can install it via
pip_ (Mac OS X / Linux) or easy_install_ (Windows) with::

    > pip install django-roughpages
    > easy_install django-roughpages

.. _pip:  https://pypi.python.org/pypi/pip
.. _easy_install: https://pythonhosted.org/setuptools/easy_install.html#installing-easy-install

Ok. Now make a tutorial project with the following command.
If you don't have ``django-admin.py``, make sure that you have a latest django
in your system::

    > django-admin.py startproject roughpagestut

The command above will create the following files and directories::

    roughpagestut/
    ├── manage.py
    └── roughpagestut
         ├── __init__.py
         ├── settings.py
         ├── urls.py
         └── wsgi.py

Then open ``roughpagestut/roughpagestut/settings.py`` and edit the settings.
Refer the sample settings below (``# ...`` indicate the cut out).

.. code:: python

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    
    INSTALLED_APPS = (
        # ... lot more
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'roughpages',
    )
    # ...
    MIDDLEWARE_CLASSES = (
        # ... lot more
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'roughpages.middleware.RoughpageFallbackMiddleware',
    )

    TEMPLATE_DIRS = (
        # roughpages/templates
        os.path.join(BASE_DIR, 'templates'),
    )

Ok now, run syncdb and server with the following commands::

    > python manage.py syncdb
    > python manage.py runserver 8000

When you access http://localhost:8000/, you will see "It worked!" page.
Confirm that accessing http://localhost:8000/info/ lead you to 404 Not found.

Ofcourse, we have not make any views yet thus there are no other pages exists.
Now let's make a static page by django-roughpages.
Create ``info.html`` file in ``templates/roughpages`` directory.
The final directory tree would be same as the below::

    roughpagestut/
    ├── manage.py
    ├── roughpagestut
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── templates
        └── roughpages
            └── info.html

Then open ``info.html`` and edit the file as followed

.. code:: html

    <html>
    <body>
        <p>Hello Rough!</p>
    </body>
    </html>

Now if you access the http://localhost:8000/info/, you will see "Hello Rough!"
page.
So django-roughpages automatically detect the corresponding template files (in
this case, ``info.html``) from the accessed URL.
If there is a corresponding template files in the template directory,
django-roughpages simply render the template and respond it.
Otherwise it re-raise the ``Http404`` exceptions for other middlewares such
as django's flatpages app.


Complex template file finding
------------------------------
django-roughpages use a backend to determine the filename from the accessed
url; the default backend is ``roughpages.backends.AuthTemplateFilenameBackend``
and the backend return two template filenames depends on the accessed users
authentication state.
Assume that the user accessed http://localhost:8000/info/, if the accessed user
is authenticated then the backend return ``roughpages/info_authenticated.html``
and ``roughpages/info.html``.
Then django-roughpages try to find the template files from the beginning of the
list, thus the order of the appearance is important.

You can find detail informations about built-in backends at :doc:`backends`.
