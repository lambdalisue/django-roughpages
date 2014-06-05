# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from django.http import Http404
from roughpages.middleware import RoughpageFallbackMiddleware
from roughpages.tests.compat import MagicMock, patch, override_settings


@override_settings(DEBUG=True)
class RoughpagesRoughpageFallbackMiddlewareTestCase(TestCase):
    def setUp(self):
        self.middleware = RoughpageFallbackMiddleware()
        self.request = MagicMock()
        self.request.session = {}
        self.request.path_info = '/foo/bar/hoge/'
        self.response = MagicMock()

    def test_middleware_with_200_response(self):
        self.response.status_code = 200
        with patch('roughpages.middleware.roughpage') as p:
            r = self.middleware.process_response(self.request,
                                                 self.response)
            # roughpage view should not be called
            self.assertFalse(p.called)
            # original response should be returend
            self.assertEqual(r, self.response)

    def test_middleware_with_404_response(self):
        self.response.status_code = 404
        with patch('roughpages.middleware.roughpage') as p:
            r = self.middleware.process_response(self.request,
                                                 self.response)
            # roughpage view should be called
            self.assertTrue(p.called)
            # roughpage view should be called with request and path_info
            p.assert_called_with(self.request, self.request.path_info)
            # roughpage return should be returned
            self.assertEqual(r, p())

    def test_middleware_with_404_response_with_404(self):
        self.response.status_code = 404
        with patch('roughpages.middleware.roughpage') as p:
            p.side_effect = Http404
            r = self.middleware.process_response(self.request,
                                                 self.response)
            # roughpage view should be called
            self.assertTrue(p.called)
            # roughpage view should be called with request and path_info
            p.assert_called_with(self.request, self.request.path_info)
            # original response should be returend
            self.assertEqual(r, self.response)

    def test_middleware_with_404_response_with_exception(self):
        self.response.status_code = 404
        with patch('roughpages.middleware.roughpage') as p:
            p.side_effect = Exception
            self.assertRaises(Exception,
                              self.middleware.process_response,
                              self.request, self.response)
            # roughpage view should be called
            self.assertTrue(p.called)
            # roughpage view should be called with request and path_info
            p.assert_called_with(self.request, self.request.path_info)

    @override_settings(DEBUG=False)
    def test_middleware_with_404_response_with_exception_NO_DEBUG(self):
        self.response.status_code = 404
        with patch('roughpages.middleware.roughpage') as p:
            p.side_effect = Exception
            r = self.middleware.process_response(self.request,
                                                 self.response)
            # roughpage view should be called
            self.assertTrue(p.called)
            # roughpage view should be called with request and path_info
            p.assert_called_with(self.request, self.request.path_info)
            # original response should be returend
            self.assertEqual(r, self.response)
