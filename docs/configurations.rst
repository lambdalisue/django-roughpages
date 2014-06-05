Configurations
===============
django-roughpages provide the following options.

``ROUGHPAGES_BACKEND``
    A class object or dots separated python import path to specify the template
    filename backend.
    The default value is ``'roughpages.backends.AuthTemplateFilenameBackend'``

``ROUGHPAGES_INDEX_FILENAME``
    A filename without extension which is used to represent the root URL
    (``'/'``).
    When the django-roughpage process the root URL, this filename is used
    instead to find the template file like ``'/.html'``.
    The default value is ``'index'``

``ROUGHPAGES_TEMPLATE_DIR``
    A directory name which is automatically prepended to the template file
    path; if the user access to http://localhost/foo/bar/hoge, the actual
    template file path would be ``'roughpages/foo/bar/hoge.html'`` when the
    ``ROUGHPAGES_TEMPLATE_DIR`` is set to ``'roughpages'``.
    The default value is ``'roughpages'``

``ROUGHPAGES_TEMPLATE_FILE_EXT``
    A file extension which is used to create template file path.
    The default value is ``'.html'``

``ROUGHPAGES_RAISE_TEMPLATE_DOES_NOT_EXISTS``
    If this is ``True`` then ``TemplateDoesNotExists`` exception would be
    throwed when a user accessed to invalid url and django-roughpages could
    not find any corresponding template files.
    This feature does not work in product mode (``DEBUG=False``) while
    django-roughpages simply return back the response in exceptions when the
    ``DEBUG`` is ``False``.
    The default value is ``False``

