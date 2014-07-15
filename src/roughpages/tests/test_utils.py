# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from roughpages.utils import (url_to_filename,
                              remove_pardir_symbols,
                              replace_dots_to_underscores_at_last)
from roughpages.tests.compat import patch


class RoughpagesUtilsTestCase(TestCase):
    def test_url_to_filename_remove_leading_slash(self):
        url = "/aaa/bbb/ccc"
        expected = "aaa/bbb/ccc"
        self.assertEqual(url_to_filename(url),
                         expected)

    def test_url_to_filename_remove_trailing_slash(self):
        url = "aaa/bbb/ccc/"
        expected = "aaa/bbb/ccc"
        self.assertEqual(url_to_filename(url),
                         expected)

    def test_url_to_filename_remove_call_remove_pardir_symbols(self):
        with patch('roughpages.utils.remove_pardir_symbols') as p:
            url_to_filename("")
            self.assertTrue(p.called)

    def test_url_to_filename_remove_call_replace_dots_to_underscores_at_last(self):
        with patch('roughpages.utils.replace_dots_to_underscores_at_last') as p:
            url_to_filename("")
            self.assertTrue(p.called)

    def test_remove_pardir_symbols_remove_pardir_symobls(self):
        path = "/../A/../B/../C/../"
        expected = "/A/B/C/"
        self.assertEqual(remove_pardir_symbols(path),
                         expected)

    def test_replace_dots_to_underscores_at_last(self):
        path = '/AA.AA.AA/BB.BB.BB/CC.CC.CC'
        expected = '/AA.AA.AA/BB.BB.BB/CC_CC_CC'
        self.assertEqual(replace_dots_to_underscores_at_last(path),
                         expected)
