# Copyright (c) 2013 Zeid Zabaneh
# PyTemplates is distributed under the terms of the GNU General Public License

import re

class Tag(object):
    def __init__(self, tag_name, *args, **kwargs):
        self.tag_name = tag_name
        self.attributes = {k: v for k, v in kwargs.iteritems()}
        self.unnamed_attributes = [v for v in args]
        for k in self.attributes:
            if k[0] == '_':
                self.attributes[k[1:]] = self.attributes[k]
                del(self.attributes[k])


def escape(s):
    s = str(s)
    return (
        s.replace('&', '&amp;')
        .replace('>', '&gt;')
        .replace('<', '&lt;')
        .replace("'", '&#39;')
        .replace('"', '&#34;')
    )


def t(arg, *args, **kwargs):
    _name = re.compile('^(\w+?)(?:\.|#|\:|\[|$)')
    _classes = re.compile('\.([a-zA-Z0-9\-_]+)')
    _id = re.compile("""#(\w+)(?=([^'"]*("|')[^'"]*("|'))*[^'"]*$)""")
    _unnamed_attrs = re.compile('\:(\w+)')
    _named_attrs0 = re.compile("""\[([a-zA-Z0-9\-\_]+?)=(.+?)\]""")
    _named_attrs1 = re.compile("""\[([a-zA-Z0-9\-\_]+?)=\"(.+?)\"\]""")
    _named_attrs2 = re.compile("""\[([a-zA-Z0-9\-\_]+?)=\'(.+?)\'\]""")

    name = _name.findall(arg)[0]
    attributes = dict()
    tag_id = _id.findall(arg)
    tag_classes = _classes.findall(arg)
    tag_unnamed_attrs = _unnamed_attrs.findall(arg)
    tag_named_attrs = _named_attrs0.findall(arg)
    tag_named_attrs += _named_attrs1.findall(arg)
    tag_named_attrs += _named_attrs2.findall(arg)

    unnamed_attributes = tag_unnamed_attrs
    named_attributes = {k: v for k, v in tag_named_attrs}
    if tag_id:
        attributes['id'] = tag_id[0][0]

    classes = ' '.join(tag_classes)

    if classes:
        attributes['_class'] = classes

    attributes.update(named_attributes)
    attributes.update(kwargs)
    unnamed_attributes += args

    return Tag(name, *unnamed_attributes, **attributes)

def render_attributes(attributes={}, unnamed_attributes=[]):
    '''
    Renders named and boolean attributes on an element.
    '''
    _attributes = ' '.join([
        '{0}="{1}"'.format(k, v) for
        k, v in attributes.iteritems()])
    _unnamed_attributes = ' '.join([
        '{0}'.format(k) for
        k in unnamed_attributes])

    attributes = "{0} {1}".format(_attributes, _unnamed_attributes).strip()
    return attributes


def fix_tag(tag):
    if type(tag) == set:
        _arg = ''
        _args = []
        _kwargs = {}
        for e in tag:
            if type(e) == str:
                _arg = e
            elif type(e) == tuple:
                if len(e) == 1:
                    _args.append(e[0])
                elif len(e) == 2:
                    _kwargs[e[0]] = e[1]

        tag = t(_arg, *_args, **_kwargs)
    return tag


def render_empty_tag(tag):
    '''
    Renders an empty html tag (e.g. <br> or <input type="text">).
    This type of tag is represented by a tuple.
    '''
    tag = fix_tag(tag)

    container = (
        "<{0} {1}>" if tag.attributes or tag.unnamed_attributes else "<{0}>")
    attributes = render_attributes(
        attributes=tag.attributes, unnamed_attributes=tag.unnamed_attributes)
    return container.format(tag.tag_name, attributes)


def render_content(tag, *args):
    '''
    Render html tags (e.g. <div></div>) and recursively generate
    all HTML content in the hierarchy.
    '''
    tag = fix_tag(tag)


    container = "<{0} {1}>{2}</{0}>" if tag.attributes or tag.unnamed_attributes else "<{0}>{2}</{0}>"
    content = str()

    # TODO check first arg of list or tuple to be Tag, else render string
    for arg in args:
        if type(arg) in (list, tuple) and arg and type(arg[0]) in (Tag, set):
            if type(arg) == list:
                content += render_content(*arg)
            elif type(arg) == tuple:
                content += render_empty_tag(*arg)
        elif type(arg) == tuple and arg and arg[0] == 'safe':
            content += arg[1].__str__()
        elif type(arg) in (list, tuple):
            for sub_arg in arg:
                if sub_arg and type(sub_arg[0]) in (Tag, set):
                    content += render_content(*sub_arg)
                else:
                    content += escape(arg.__str__())
        else:
            content += escape(arg.__str__())

    return container.format(
        tag.tag_name,
        render_attributes(
            attributes=tag.attributes, unnamed_attributes=tag.unnamed_attributes),
        content)

