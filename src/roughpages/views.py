# coding=utf-8
"""
Roughpage views
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
from django.http import Http404, HttpResponse
from django.template import loader, RequestContext, TemplateDoesNotExist
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from roughpages.conf import settings
from roughpages.backends import get_backend
from roughpages.utils import url_to_filename

# This view is called from RoughpageFallbackMiddleware.process_response
# when a 404 is raised, which often means CsrfViewMiddleware.process_view
# has not been called even if CsrfViewMiddleware is installed. So we need
# to use @csrf_protect, in case the template needs {% csrf_token %}.
# However, we can't just wrap this view; if no matching roughpage exists,
# or a redirect is required for authentication, the 404 needs to be returned
# without any CSRF checks. Therefore, we only
# CSRF protect the internal implementation.


def roughpage(request, url):
    """
    Public interface to the rough page view.
    """
    if settings.APPEND_SLASH and not url.endswith('/'):
        # redirect to the url which have end slash
        return redirect(url + '/', permanent=True)
    # get base filename from url
    filename = url_to_filename(url)
    # try to find the template_filename with backends
    template_filenames = get_backend().prepare_filenames(filename,
                                                         request=request)
    # add extra prefix path
    root = settings.ROUGHPAGES_TEMPLATE_DIR
    template_filenames = [os.path.join(root, x) for x in template_filenames]
    try:
        t = loader.select_template(template_filenames)
        return render_roughpage(request, t)
    except TemplateDoesNotExist:
        if settings.ROUGHPAGES_RAISE_TEMPLATE_DOES_NOT_EXISTS:
            raise
        raise Http404


@csrf_protect
def render_roughpage(request, t):
    """
    Internal interface to the rough page view.
    """
    import django
    if django.VERSION >= (1, 8):
        c = {}
        response = HttpResponse(t.render(c, request))
    else:
        c = RequestContext(request)
        response = HttpResponse(t.render(c))
    return response
