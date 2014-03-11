.. Pytemplates documentation master file, created by
   sphinx-quickstart on Wed Dec 18 22:36:32 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pytemplates Documentation
=======================================
Pytemplates is a lightweight HTML template engine written in Python.

Features
--------
- Pure Python Syntax
- Template Inheritance
- Blocks
- Macros
- Context
- Comes with a Django plugin


Installation Instructions
-------------------------
To install pytemplates, run ``pip install pytemplates``.

Django Plugin
+++++++++++++
To use the Django plugin, import the *render_to_response* function included in the *django_plugin* module and use it in your views.


Basic Syntax
------------
Elements
++++++++
An element must be placed in a list or a tuple. The first entry in the list or tuple must be the tag definition, and is placed in a set. The second entry is the content of that element. ::

    [{'div'}, "I am a div element."]

Tags
++++
A tag is the first entry in an element. Attributes are passed in as tuples, or written in short form. Content is the second entry in the element. ::

    # Long form
    # Putting your element in a tuple will create a html element with no closing tag
    ({'input', ('value', 'This is a disabled input field'), ('disabled',)},)

    # Output: <input value="This is a disabled input field" disabled>

    # Putting your element in a list will create an html element with a closing tag
    [{'ul', ('class', 'unstyled'), ('id', 'my_list')},
        [{'li'}, 'One'],
        [{'li'}, 'Two'],
    ]

    # Output: <ul class="unstyled" id="my_list"><li>One</li><li>Two</li></ul>

    # Short form
    ({'input[value="This is a disabled input field"]:disabled'},)

    [{'ul#my_list.unstyled'},
        [{'li'}, 'One'],
        [{'li'}, 'Two'],
    ]

Template
++++++++
Your template is a class that extends the Template class. ::

    from pytemplates.pytemplates import Template
    class MyTemplate(Template):
        def template(self, *args):
            # Your template code goes here and is returned by this method
            template = [{'div'}, "Hello"]
            return template

Context
+++++++
Context is passed in from your view when you call your render function. It is also accessible from the instance ::

    # In your views.py
    class MyView(TemplateView):
        def get(self, request, *args):
            context = {'test': 'Hello World'}
            return render_to_response(request, 'my_template', context)

    #### In your template file:
    class MyTemplate(Template):
        def template(self, *args):
            c = self.context
            template = [{'div'}, c['test']]
            return template

Blocks
++++++
A block is defined as an instance method inside your template, with the **@block** decorator. Blocks are passed to your template function and are accessible from the instance. ::

    from pytemplates.pytemplates import Template, block
    class MyTemplate(Template):
        @block
        def my_block(self, *args):
            return [{'span'}, "It works!"]

        def template(self, *args):
            b = self.blocks
            # You can access all your blocks from variable b
            template = [{'div'}, b.my_block]
            return template

    class MyOtherTemplate(MyTemplate):
        @block
        def my_block(self, *args):
            # You can also access the context in your blocks
            c = self.context
            return [{'div'}, c['test']]

Macros
++++++
A macro is any function that returns valid template code. You must use the **@macro** decorator to let your template know about your macro.

You can also group many macros as static methods inside a class that is decorated with the **@macro** decorator as well. ::

    from pytemplates.pytemplates import Template, macro
    class MyTemplate(Template):
        @macro
        def list_maker(n):
            out = [{'ul'}] + [
                [{'li'}, i] for i in range(n)
            ]
            return out

        def template(self, c, b, m):
            template = [{'div'}, m.list_maker(10)]
            return template

Includes
++++++++
You can include any external file with an include statement. This will render that file wherever you put the include statement. This can be used to include embedded javascript code, css code, or raw html code, or any other text you would like to include in your templates. ::

    from pytemplates.pytemplates import Template
    class MyTemplate(Template):
        def template(self, c, b, m):
            template = [{'div'}, self.include('some_external_file.html')]
            return template


Rendering the Template
++++++++++++++++++++++
To render your template, create an instance of the template and call its render() function. ::

    template = MyTemplate()

    # This will output the rendered HTML template
    template.render()

    # You can pass the context to the render function as a dictionary:
    template.render({'some_variable': 1234})


Full Example
++++++++++++
::

    ### In your views.py
    from pytemplates.django_plugin import render_to_response
    from django.views.generic.base import TemplateView

    class MyView(TemplateView):
        def get(self, request, *args):
            context_test = {'test': '<strong>Hello World</strong>'}
            return render_to_response(request, 'templates.test_template', context_test)


    ### In your urls.py
    from myapp.views import MyView
    urlpatterns = patterns('',
        url(r'^$', MyView.as_view(), name='home'),
    )


    ### In templates/test_template.py
    from pytemplates.pytemplates import Template
    from pytemplates.pytemplates import block
    from pytemplates.pytemplates import macro
    from pytemplates.pytemplates import render


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


.. toctree::
   :maxdepth: 2
