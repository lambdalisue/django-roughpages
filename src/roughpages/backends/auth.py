# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from roughpages.backends.base import TemplateFilenameBackendBase
from roughpages.backends.decorators import prepare_filename_decorator


class AuthTemplateFilenameBackend(TemplateFilenameBackendBase):
    """
    A TemplateFilenameBackend which return filename with authenticated state
    suffix.
    """

    @prepare_filename_decorator
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
            >>> backend = AuthTemplateFilenameBackend()
            >>> request.user.is_authenticated.return_value = True
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
            >>> request.user.is_authenticated.return_value = True
            >>> filenames = backend.prepare_filenames('',
            ...                                       request)
            >>> assert filenames == [
            ...     'index_authenticated.html',
            ...     'index.html'
            ... ]
            >>> request.user.is_authenticated.return_value = False
            >>> filenames = backend.prepare_filenames('',
            ...                                       request)
            >>> assert filenames == [
            ...     'index_anonymous.html',
            ...     'index.html'
            ... ]
        """
        filenames = [normalized_url]
        if request.user.is_authenticated():
            filenames.insert(0, normalized_url + ".authenticated")
        else:
            filenames.insert(0, normalized_url + ".anonymous")
        return filenames
