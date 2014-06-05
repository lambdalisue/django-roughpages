# coding=utf-8
"""
Roughpage template filename backends
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from functools import wraps


def get_backend(backend_class=None):
    """
    Get backend instance

    If no `backend_class` is specified, the backend class is determined from
    the value of `settings.ROUGHPAGES_BACKEND`.
    `backend_class` can be a class object or dots separated python import path

    Returns:
        backend instance
    """
    from roughpages.conf import settings
    from roughpages.compat import import_module
    cache_name = '_backend_instance'
    if not hasattr(get_backend, cache_name):
        backend_class = backend_class or settings.ROUGHPAGES_BACKEND
        if isinstance(backend_class, basestring):
            module_path, class_name = backend_class.rsplit(".", 1)
            module = import_module(module_path)
            backend_class = getattr(module, class_name)
        setattr(get_backend, cache_name, backend_class())
    return getattr(get_backend, cache_name)


def prepare_filename_extensions(fn):
    """
    A decorator to append filename extensions to filenames
    """
    @wraps(fn)
    def inner(self, normalized_url, request):
        filenames = fn(self, normalized_url, request)
        filenames = [x + ext for x in filenames if x]
        return filenames
    from roughpages.conf import settings
    ext = settings.ROUGHPAGES_TEMPLATE_FILE_EXT
    return inner


class TemplateFilenameBackendBase(object):
    """
    A base class of TemplateFilenameBackend
    """
    def prepare_filenames(self, normalized_url, request):
        """
        Prepare template filename list

        Args:
            normalized_url (str): A normalized url
            request (instance): An instance of HttpRequest

        Returns:
            list

        Raises:
            NotImplementedError
        """
        raise NotImplementedError(
            "Subclass of TemplateFilenameBackendBase need to "
            "override 'prepare_filename' method.")


class PlainTemplateFilenameBackend(TemplateFilenameBackendBase):
    """
    A TemplateFilenameBackend which simply return filename single list
    """

    @prepare_filename_extensions
    def prepare_filenames(self, normalized_url, request):
        """
        Prepare template filename list

        Args:
            normalized_url (str): A normalized url
            request (instance): An instance of HttpRequest

        Returns:
            list

        Examples:
            >>> from mock import MagicMock
            >>> request = MagicMock()
            >>> backend = PlainTemplateFilenameBackend()
            >>> filenames = backend.prepare_filenames('foo/bar/hogehoge',
            ...                                       request)
            >>> assert filenames == [
            ...     'foo/bar/hogehoge.html'
            ... ]
        """
        return [normalized_url]


class AuthTemplateFilenameBackend(TemplateFilenameBackendBase):
    """
    A TemplateFilenameBackend which return filename with authenticated state
    suffix.
    """

    @prepare_filename_extensions
    def prepare_filenames(self, normalized_url, request):
        """
        Prepare template filename list based on the user authenticated state

        If user is authenticated user, it use '_authenticated' as a suffix.
        Otherwise it use '_anonymous' as a suffix to produce the template
        filename list. The list include original filename at the end of the
        list.

        Args:
            normalized_url (str): A normalized url
            request (instance): An instance of HttpRequest

        Returns:
            list

        Examples:
            >>> from mock import MagicMock
            >>> request = MagicMock()
            >>> request.user.is_authenticated.return_value = True
            >>> backend = AuthTemplateFilenameBackend()
            >>> filenames = backend.prepare_filenames('foo/bar/hogehoge',
            ...                                       request)
            >>> assert filenames == [
            ...     'foo/bar/hogehoge_authenticated.html',
            ...     'foo/bar/hogehoge.html'
            ... ]
            >>> request.user.is_authenticated.return_value = False
            >>> filenames = backend.prepare_filenames('foo/bar/hogehoge',
            ...                                       request)
            >>> assert filenames == [
            ...     'foo/bar/hogehoge_anonymous.html',
            ...     'foo/bar/hogehoge.html'
            ... ]
        """
        filenames = [normalized_url]
        if request.user.is_authenticated():
            filenames.insert(0, normalized_url + "_authenticated")
        else:
            filenames.insert(0, normalized_url + "_anonymous")
        return filenames


if __name__ == '__main__':
    import doctest
    doctest.testmod()
