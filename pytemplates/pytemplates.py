# Copyright (c) 2013 Zeid Zabaneh
# PyTemplates is distributed under the terms of the GNU General Public License

from utils import escape
from utils import render_empty_tag
from utils import render_content
from utils import t
from utils import Tag

from collections import defaultdict
import re


def macro(f):
    setattr(f, 'template_macro', True)
    return f


def block(f):
    setattr(f, 'template_block', True)
    return f


def render(variable, *args):
    if 'safe' in args:
        return variable
    else:
        return escape(variable.__str__())


class Blocks(object):
    pass


class Macros(object):
    pass


class Tags(object):
    def __getattr__(self, name):
        return lambda *args, **kwargs: Tag(name, *args, **kwargs)


class Template(object):
    def __init__(self, dd=True, *args, **kwargs):
        self.doctype = "html"

        if hasattr(self, 'extra_macros'):
            for macro in self.extra_macros:
                setattr(self, macro.__name__, macro)

        self.context = defaultdict(str) if dd else dict()
        self.blocks = Blocks()
        self.macros = Macros()
        self._register_macros()
        self._register_blocks()

    def _register_blocks(self):
        members = ((k, getattr(self, k)) for k in dir(self) if
                   getattr(getattr(self, k), 'template_block', None))
        for k, v in members:
            setattr(self.blocks, k.lower(), v(*self._prepare()))

    def _register_macros(self):
        members = ((k, getattr(self, k)) for k in dir(self) if
                   getattr(getattr(self, k), 'template_macro', None))
        for k, v in members:
            setattr(self.macros, k.lower(), v)

    def template(self):
        pass

    def _context(self, context):
        for k, v in context.iteritems():
            self.context[k] = v

    def _prepare(self):
        return [self.context, self.blocks, self.macros]

    def include(self, file_name):
        f = open(file_name, 'r')
        string = f.read()
        return string

    def render(self, context=None):
        if context:
            self._context(context)
        template = self.template(*self._prepare())
        output = render_content(*template)
        if self.doctype:
            t = Tags()
            output = render_empty_tag(
                getattr(t, '!DOCTYPE')(self.doctype)) + output
        return output
