# coding=utf-8
"""
django-permission application configure
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
__all__ = ('settings',)
from django.conf import settings
from appconf import AppConf


class RoughpageConf(AppConf):
    # An backend class path
    BACKEND = 'roughpages.backends.AuthTemplateFilenameBackend'

    # A special filename without extension indicate the root '/'
    INDEX_FILENAME = 'index'

    # A template filename located directory
    TEMPLATE_DIR = 'roughpages'

    # A template filename extension string
    TEMPLATE_FILE_EXT = '.html'

    # Raise TemplateDoesNotExist exception
    RAISE_TEMPLATE_DOES_NOT_EXISTS = False
