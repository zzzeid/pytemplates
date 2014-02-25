# Copyright (c) 2013 Zeid Zabaneh
# PyTemplates is distributed under the terms of the GNU General Public License

from django.http import HttpResponse
from django.template import RequestContext
from django.template.base import Context
import inspect
from importlib import import_module

import os
from django.template import Context, TemplateDoesNotExist
from django.utils.translation import gettext_lazy as _


class Loader(object):
    def get_template(self, template):
        return Adapter([template])

    def select_template(self, templates):
        return Adapter(templates)

class Adapter(object):
    def __init__(self, names):
        self.names = names

    def render(self, variables={}):
        import os
        if isinstance(variables, Context):
            result = {}
            for d in [d for d in variables].__reversed__():
                result.update(d)
            variables = result
        for name in self.names:
            try:
                _template = import_module('{0}'.format(name))
                template = inspect.getmembers(_template, inspect.isclass)[0][1]()
                return template.render(variables)
            except ImportError:
                _module = name.split('.')
                name = _module[-1:][0]
                _module = '.'.join(_module[:-1])
                _template = import_module('{0}'.format(_module))
                for _class in inspect.getmembers(_template, inspect.isclass):
                    if _class[0] == name:
                        template = _class[1]()
                        return template.render(variables)

loader = Loader()

def render_to_response(request, template, variables=None, **kwargs):
    rendered = render_to_string(template, variables, context_instance=RequestContext(request))
    try:
        return HttpResponse(rendered, **kwargs)
    except Exception as e:
        print "**", e

def render_to_string(template, variables=None, *args, **kwargs):
    loader = Loader()
    t = loader.get_template(template)
    context_instance = kwargs.get('context_instance')
    if not context_instance:
        return t.render(Context(variables))
    context_instance.update(variables)
    return t.render(context_instance)
