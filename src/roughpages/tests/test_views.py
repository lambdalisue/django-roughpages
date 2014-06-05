# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from django.http import Http404
from django.template import TemplateDoesNotExist
from roughpages.tests.compat import MagicMock, override_settings
from roughpages.tests.compat import patch, DEFAULT
from roughpages.views import render_roughpage, roughpage


@override_settings(
    ROUGHPAGES_BACKEND='roughpages.backends.PlainTemplateFilenameBackend',
    ROUGHPAGES_TEMPLATE_DIR='roughpages',
    ROUGHPAGES_TEMPLATE_FILE_EXT='.html',
    ROUGHPAGES_RAISE_TEMPLATE_DOES_NOT_EXISTS=False,
)
class RoughpagesViewsTestCase(TestCase):
    def setUp(self):
        self.request = MagicMock()
        self.request.session = {}

    @patch.multiple('roughpages.views',
                    RequestContext=DEFAULT,
                    HttpResponse=DEFAULT)
    def test_render_roughpage(self, RequestContext, HttpResponse):
        t = MagicMock()
        r = render_roughpage(self.request, t)
        # RequestContext should be initialized with request
        RequestContext.assert_called_with(self.request)
        # t.render should be called with the context
        t.render.assert_called_with(RequestContext())
        # HttpResponse should be initialized with the output of
        # t.render(c)
        HttpResponse.assert_called_with(t.render(RequestContext()))
        # return should be response
        self.assertEqual(r, HttpResponse())

    @patch.multiple('roughpages.views',
                    loader=DEFAULT,
                    render_roughpage=DEFAULT)
    def test_roughpage(self, loader, render_roughpage):
        url = '/foo/bar/hoge/'
        r = roughpage(self.request, url)
        # loader.select_template should be called with follow
        # because backend is PlainTemplateFilenameBackend
        template_filenames = ['roughpages/foo/bar/hoge.html']
        loader.select_template.assert_called_with(template_filenames)
        # render_roughpage should be called with
        t = loader.select_template()
        render_roughpage.assert_called_with(self.request, t)
        # should return the return of render_roughpage
        self.assertEqual(r, render_roughpage())

    @patch.multiple('roughpages.views',
                    loader=DEFAULT,
                    render_roughpage=DEFAULT)
    def test_roughpage_no_template(self, loader, render_roughpage):
        loader.select_template.side_effect = TemplateDoesNotExist
        url = '/foo/bar/hoge/'
        self.assertRaises(Http404,
                          roughpage,
                          self.request, url)
        # loader.select_template should be called with follow
        # because backend is PlainTemplateFilenameBackend
        template_filenames = ['roughpages/foo/bar/hoge.html']
        loader.select_template.assert_called_with(template_filenames)

    @override_settings(
        ROUGHPAGES_RAISE_TEMPLATE_DOES_NOT_EXISTS=True)
    @patch.multiple('roughpages.views',
                    loader=DEFAULT,
                    render_roughpage=DEFAULT)
    def test_roughpage_no_template_raise(self, loader, render_roughpage):
        loader.select_template.side_effect = TemplateDoesNotExist
        url = '/foo/bar/hoge/'
        self.assertRaises(TemplateDoesNotExist,
                          roughpage,
                          self.request, url)
        # loader.select_template should be called with follow
        # because backend is PlainTemplateFilenameBackend
        template_filenames = ['roughpages/foo/bar/hoge.html']
        loader.select_template.assert_called_with(template_filenames)