# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from roughpages.conf import settings
from roughpages.compat import import_module


def get_backend(backend_class=None):
    """
    Get backend instance

    If no `backend_class` is specified, the backend class is determined from
    the value of `settings.ROUGHPAGES_BACKEND`.
    `backend_class` can be a class object or dots separated python import path

    Returns:
        backend instance
    """
    cache_name = '_backend_instance'
    if not hasattr(get_backend, cache_name):
        backend_class = backend_class or settings.ROUGHPAGES_BACKEND
        if isinstance(backend_class, basestring):
            module_path, class_name = backend_class.rsplit(".", 1)
            module = import_module(module_path)
            backend_class = getattr(module, class_name)
        setattr(get_backend, cache_name, backend_class())
    return getattr(get_backend, cache_name)


from roughpages.backends.decorators import prepare_filename_decorator
from roughpages.backends.base import TemplateFilenameBackendBase
from roughpages.backends.plain import PlainTemplateFilenameBackend
from roughpages.backends.auth import AuthTemplateFilenameBackend
