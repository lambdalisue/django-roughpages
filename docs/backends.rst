Backends
=========
django-roughpages provde the following backends.
All backends are located in ``roughpages.backends`` module.


``TemplateFilenameBackendBase``
    A backend interface class. Developer can create a custom backend by
    inheriting this class.
    The subclass must override
    ``prepare_filenames(self, normalized_url, request)`` method to provide
    the template filename list.

``PlainTemplateFilenameBackend``
    A simple backend. This backend just return the corresponding filename of
    URL (http://localhost:8000/foo/bar/hoge/ to ``'foo/bar/hoge.html'``).
    However, it will return ``['index.html']`` when the user accessed to the root
    of the site (the filename is determined by
    ``settings.ROUGHPAGES_INDEX_FILENAME`` value).

``AuthTemplateFilenameBackend``
    A backend which lookup the accessed users authentication state.
    If the user is authenticated, the backend return
    ``<something>_authenticated.html`` and ``<something>.html``.
    Otherwise it return ``<something>_anonymous.html`` and
    ``<something>.html``.
    Additionally it will return ``['index_authenticated.html', 'index.html']``
    or ``['index_anonymous.html', 'index.html']`` when the user accessed to the
    root of the site (the filename is determined by
    ``settings.ROUGHPAGES_INDEX_FILENAME`` value).
