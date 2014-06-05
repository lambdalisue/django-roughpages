# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from roughpages.backends.base import TemplateFilenameBackendBase
from roughpages.backends.decorators import prepare_filename_decorator


class PlainTemplateFilenameBackend(TemplateFilenameBackendBase):
    """
    A TemplateFilenameBackend which simply return filename single list
    """

    @prepare_filename_decorator
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
            >>> filenames = backend.prepare_filenames('',
            ...                                       request)
            >>> assert filenames == [
            ...     'index.html'
            ... ]
        """
        return [normalized_url]
