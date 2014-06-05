# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from roughpages import backends
from roughpages.tests.compat import MagicMock, override_settings

TEMPLATE_FILENAME = 'foo/bar/hogehoge.html'
ANONYMOUS_TEMPLATE_FILENAME = 'foo/bar/hogehoge_anonymous.html'
AUTHENTICATED_TEMPLATE_FILENAME = 'foo/bar/hogehoge_authenticated.html'

ANONYMOUS_REQUEST = MagicMock()
ANONYMOUS_REQUEST.user.is_authenticated.return_value = False
AUTHENTICATED_REQUEST = MagicMock()
AUTHENTICATED_REQUEST.user.is_authenticated.return_value = True


@override_settings(
    ROUGHPAGES_BACKEND='roughpages.backends.AuthTemplateFilenameBackend',
)
class RoughpagesBackendsTestCase(TestCase):
    def setUp(self):
        # clear cache
        if hasattr(backends.get_backend, '_backend_instance'):
            del backends.get_backend._backend_instance

    def test_get_backend(self):
        backend = backends.get_backend()
        self.assertTrue(isinstance(backend,
                                   backends.AuthTemplateFilenameBackend))

    def test_get_backend_with_string(self):
        backend = backends.get_backend(
            'roughpages.backends.PlainTemplateFilenameBackend')
        self.assertTrue(isinstance(backend,
                                   backends.PlainTemplateFilenameBackend))

    def test_get_backend_with_instance(self):
        backend = backends.get_backend(backends.PlainTemplateFilenameBackend)
        self.assertTrue(isinstance(backend,
                                   backends.PlainTemplateFilenameBackend))


class RoughpagesTemplateFilenameBackendBaseTestCase(TestCase):
    def setUp(self):
        self.backend = backends.TemplateFilenameBackendBase()
        self.request = MagicMock()

    def test_prepare_filenames_raise_exception(self):
        """prepare_filenames should raise NotImplementedError"""
        self.assertRaises(NotImplementedError,
                          self.backend.prepare_filenames,
                          TEMPLATE_FILENAME,
                          AUTHENTICATED_REQUEST)


class RoughpagesPlainTemplateFilenameBackendTestCase(TestCase):
    def setUp(self):
        self.backend = backends.PlainTemplateFilenameBackend()

    def test_prepare_filenames_return_correct_list(self):
        """prepare_filenames should return a list with original filename"""
        r = self.backend.prepare_filenames(TEMPLATE_FILENAME,
                                           AUTHENTICATED_REQUEST)
        self.assertEqual(r, [TEMPLATE_FILENAME])


class RoughpagesAuthTemplateFilenameBackendTestCase(TestCase):
    def setUp(self):
        self.backend = backends.AuthTemplateFilenameBackend()

    def test_prepare_filenames_with_anonymous(self):
        """prepare_filenames should return a list for anonymous user"""
        r = self.backend.prepare_filenames(TEMPLATE_FILENAME,
                                           ANONYMOUS_REQUEST)
        self.assertEqual(r, [
            ANONYMOUS_TEMPLATE_FILENAME,
            TEMPLATE_FILENAME,
        ])

    def test_prepare_filenames_with_authenticated(self):
        """prepare_filenames should return a list for authenticated user"""
        r = self.backend.prepare_filenames(TEMPLATE_FILENAME,
                                           AUTHENTICATED_REQUEST)
        self.assertEqual(r, [
            AUTHENTICATED_TEMPLATE_FILENAME,
            TEMPLATE_FILENAME,
        ])

