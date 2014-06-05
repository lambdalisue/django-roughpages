# coding=utf-8
"""
Roughpage template filename backends
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os


def get_backend(backend_class=None):
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


class TemplateFilenameBackendBase(object):
    """
    A base class of TemplateFilenameBackend
    """
    def prepare_filenames(self, filename, request):
        """
        Prepare template filename list

        Args:
            filename (str): A base filename
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
    def prepare_filenames(self, filename, request):
        """
        Prepare template filename list

        Args:
            filename (str): A base filename
            request (instance): An instance of HttpRequest

        Returns:
            list

        Examples:
            >>> from mock import MagicMock
            >>> request = MagicMock()
            >>> backend = PlainTemplateFilenameBackend()
            >>> filenames = backend.prepare_filenames('foo/bar/hogehoge.html',
            ...                                       request)
            >>> assert filenames == [
            ...     'foo/bar/hogehoge.html'
            ... ]
        """
        return [filename]


class AuthTemplateFilenameBackend(TemplateFilenameBackendBase):
    """
    A TemplateFilenameBackend which return filename with authenticated state
    suffix.
    """
    def prepare_filenames(self, filename, request):
        """
        Prepare template filename list based on the user authenticated state

        If user is authenticated user, it use '_authenticated' as a suffix.
        Otherwise it use '_anonymous' as a suffix to produce the template
        filename list. The list include original filename at the end of the
        list.

        Args:
            filename (str): A base filename
            request (instance): An instance of HttpRequest

        Returns:
            list

        Examples:
            >>> from mock import MagicMock
            >>> request = MagicMock()
            >>> request.user.is_authenticated.return_value = True
            >>> backend = AuthTemplateFilenameBackend()
            >>> filenames = backend.prepare_filenames('foo/bar/hogehoge.html',
            ...                                       request)
            >>> assert filenames == [
            ...     'foo/bar/hogehoge_authenticated.html',
            ...     'foo/bar/hogehoge.html'
            ... ]
            >>> request.user.is_authenticated.return_value = False
            >>> filenames = backend.prepare_filenames('foo/bar/hogehoge.html',
            ...                                       request)
            >>> assert filenames == [
            ...     'foo/bar/hogehoge_anonymous.html',
            ...     'foo/bar/hogehoge.html'
            ... ]
        """
        basename, ext = os.path.splitext(filename)
        filenames = [filename]
        if request.user.is_authenticated():
            filenames.insert(0, "%s_authenticated%s" % (basename, ext))
        else:
            filenames.insert(0, "%s_anonymous%s" % (basename, ext))
        return filenames


if __name__ == '__main__':
    import doctest
    doctest.testmod()
