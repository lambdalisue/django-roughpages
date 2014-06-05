# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'


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

