# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from functools import wraps
from roughpages.conf import settings


def prepare_filename_decorator(fn):
    """
    A decorator of `prepare_filename` method

    1. It automatically assign `settings.ROUGHPAGES_INDEX_FILENAME` if the
       `normalized_url` is ''.
    2. It automatically assign file extensions to the output list.
    """
    @wraps(fn)
    def inner(self, normalized_url, request):
        ext = settings.ROUGHPAGES_TEMPLATE_FILE_EXT
        if not normalized_url:
            normalized_url = settings.ROUGHPAGES_INDEX_FILENAME
        filenames = fn(self, normalized_url, request)
        filenames = [x + ext for x in filenames if x]
        return filenames
    return inner
