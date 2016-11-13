# coding=utf-8
"""
Roughpage Middleware

Ref: https://github.com/django/django/blob/master/
     django/contrib/flatpages/middleware.py
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.http import Http404
from roughpages.conf import settings
from roughpages.views import roughpage

try:
    # Support a new-middleware/old-middleware
    # Ref: https://docs.djangoproject.com/ja/1.10/topics/http/middleware/#upgrading-middleware
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class RoughpageFallbackMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code != 404:
            # Non 404 response should not be treated with this middleware
            return response
        try:
            return roughpage(request, request.path_info)
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return response
        except Exception:
            if settings.DEBUG:
                raise
            return response
