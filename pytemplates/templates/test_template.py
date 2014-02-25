from pytemplates import Template
from pytemplates import block
from pytemplates import macro
from pytemplates import render


# You can define macros inside or outside the template
# If you define them outside, just put them in a list
# called "extra_macros" in your class.
@macro
def select(name, options=[], value=None):
    # Render a select field
    out = [_.select()] + [
        [_.option('checked' if o[0] == value else '', value=o[0]),
        o[1]] for o in options]
    return out


# You can also define a group of macros under a class (e.g. to group related macros)
@macro
class group_of_macros:
    @staticmethod
    def macro1():
        return [{'div'}, "macro_1"]
    @staticmethod
    def macro2():
        return [{'div'}, "macro_2"]
    @staticmethod
    def macro3():
        return [{'div'}, "macro_3"]


# This is the actual template
class MyTemplate(Template):
    extra_macros = [group_of_macros, select]

    # Blocks can be overridden in any class extending Template
    @block
    def title(*args):
        content = "It works!"
        return content

    def template(self, c, b, m):
        # c, b, and m are variables that contain the context,
        # blocks, and macros available respectively. They are also
        # accessible from self.context, self.macros, and self.blocks
        template = \
            [{'html'},
                [{'head'},
                    [{'title'}, b.title],
                    ({'link',
                        ('rel', "stylesheet"),
                        ('href', "//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css")},),
                    ({'link',
                        ('rel', "stylesheet"),
                        ('href', "http://getbootstrap.com/examples/starter-template/starter-template.css")},),
                    [{'script',
                        ('src', "//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js")},],
                ],
                [{'body'},
                    [{'div.navbar.navbar-inverse.navbar-fixed-top'},
                        [{'div.container'},
                            [{'div.navbar-header'},
                                [{'a.navbar-brand', ('href', '#')}, "PyTemplates Test"],
                            ],
                        ],
                    ],
                    [{'div.container'},
                        [{'div.starter-template'},
                            [{'button.btn:disabled'}, "I'm a disabled button!"],
                            [{'input.form-control', ('disabled',), ('value', "I'm a disabled input field.")}],
                            [{'h1'}, "Hello World!"],
                            [{'p'},
                                ('safe', """This is just an example template using <strong>PyTemplates</strong>,
                                    <strong>Bootstrap</strong>, and <strong>Django</strong>.""")],

                            # Here's an example of an if statement that will test context variable 'test':
                            ('test' in c) * [{'p'},('safe',
                                "You passed {0} as context variable 'test'".format(
                                    c['test']))] or [{'p'}, "You did not pass 'test' in the context"],
                        ],
                        m.group_of_macros.macro1(),
                        m.group_of_macros.macro2(),
                        m.group_of_macros.macro3(),
                    ],
                ]
            ]
        return template
