# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from roughpages import backends
from roughpages.tests.compat import MagicMock, override_settings


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
                          'foo/bar/hoge',
                          self.request)


class RoughpagesPlainTemplateFilenameBackendTestCase(TestCase):
    def setUp(self):
        self.backend = backends.PlainTemplateFilenameBackend()
        self.request = MagicMock()

    def test_prepare_filenames(self):
        """prepare_filenames should return a list with original filename"""
        r = self.backend.prepare_filenames('foo/bar/hoge',
                                           self.request)
        self.assertEqual(r, ['foo/bar/hoge.html'])

    def test_prepare_filenames_index(self):
        """prepare_filenames should return a list with original filename"""
        r = self.backend.prepare_filenames('',
                                           self.request)
        self.assertEqual(r, ['index.html'])


class RoughpagesAuthTemplateFilenameBackendTestCase(TestCase):
    def setUp(self):
        self.backend = backends.AuthTemplateFilenameBackend()
        self.annonymous_request = MagicMock()
        self.annonymous_request.user.is_authenticated.return_value = False
        self.authenticated_request = MagicMock()
        self.authenticated_request.user.is_authenticated.return_value = True

    def test_prepare_filenames_with_anonymous(self):
        """prepare_filenames should return a list for anonymous user"""
        r = self.backend.prepare_filenames('foo/bar/hoge',
                                           self.annonymous_request)
        self.assertEqual(r, [
            'foo/bar/hoge.anonymous.html',
            'foo/bar/hoge.html',
        ])

    def test_prepare_filenames_with_anonymous_index(self):
        """prepare_filenames should return a list for anonymous user"""
        r = self.backend.prepare_filenames('',
                                           self.annonymous_request)
        self.assertEqual(r, [
            'index.anonymous.html',
            'index.html',
        ])

    def test_prepare_filenames_with_authenticated(self):
        """prepare_filenames should return a list for authenticated user"""
        r = self.backend.prepare_filenames('foo/bar/hoge',
                                           self.authenticated_request)
        self.assertEqual(r, [
            'foo/bar/hoge.authenticated.html',
            'foo/bar/hoge.html',
        ])

    def test_prepare_filenames_with_authenticated_index(self):
        """prepare_filenames should return a list for authenticated user"""
        r = self.backend.prepare_filenames('',
                                           self.authenticated_request)
        self.assertEqual(r, [
            'index.authenticated.html',
            'index.html',
        ])
