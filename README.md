PyTemplates is a lightweight HTML template engine written in Python.


# Features
* Pure Python Syntax
* Template Inheritance
* Blocks
* Macros
* Context
* Comes with a Django plugin

# Installation Instructions
To install PyTemplates, run **pip install pytemplates** or download the package manually and run **python setup.py install**

To use the Django plugin, import the render\_to\_response function included in the django\_plugin module and use it in your views.


# Basic Syntax

## Elements
An element must be placed in a list or a tuple. The first entry in the list or tuple must be the tag definition, and is placed in a set. The second entry is the content of that element.

```python
[{'div'}, "I am a div element."]
```

## Tags
A tag is the first entry in an element. Attributes are passed in as tuples, or written in short form. Content is the second entry in the element.

### Long form
```python
({'input', ('value', 'This is a disabled input field'), ('disabled',)})
```

```python
[{'ul', ('class', 'unstyled'), ('id', 'my_list')},
    [{'li'}, 'First'],
    [{'li'}, 'Second'],
    [{'li'}, 'Third'],
]
```

### Short form
```python
({'input[value="This is a disabled input field"]:disabled'})
```

```python
[{'ul#my_list.unstyled'},
    [{'li'}, 'First'],
    [{'li'}, 'Second'],
    [{'li'}, 'Third'],
]
```

## Template
Your template is a class that extends the Template class.
```python
from pytemplates.pytemplates import Template

class MyTemplate(Template):
    def template(self, c, b, m):
        # Your template code goes here and is returned by this method
        template = [{'div'}, "Hello"]
        return template
```

## Context
Context is passed in from your view when you call your render function.
#### In your views.py
```python
class MyView(TemplateView):
    def get(self, request, *args):
        context = {'test': 'Hello World'}
        return render_to_response(request, 'my_template', context)
```

#### In your template file:
```python
class MyTemplate(Template):
    def template(self, c, b, m):
        # Context is the second argument passed to this method
        template = [{'div'}, c['test']]
        return template
```

## Blocks
A block is defined as an instance method inside your template, with the **@block** decorator. Blocks are passed to your template function as the third argument **b**.
```python
from pytemplates.pytemplates import Template, block

class MyTemplate(Template):
    @block
    def my_block(self, *args):
        return [{'span'}, "It works!"]

    def template(self, c, b, m):
        # You can access all your blocks from variable b
        template = [{'div'}, b.my_block]
        return template

class MyOtherTemplate(MyTemplate):
    @block
    def my_block(self, *args):
        # You can also access the context in your blocks
        c = self.context
        return [{'div'}, c['test']]
```

## Macros
A macro is any function that returns valid template code. You must use the **@macro** decorator to let your template know about your macro.

You can also group many macros as static methods inside a class that is decorated with the **@macro** decorator as well.

```python
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
```

## Includes
You can include any external file with an include statement. This will render that file wherever you put the include statement. This can be used to include embedded javascript code, css code, or raw html code, or any other text you would like to include in your templates.

```python
from pytemplates.pytemplates import Template

class MyTemplate(Template):
    def template(self, c, b, m):
        template = [{'div'}, self.include('some_external_file.html')]
        return template
```

# How to Create a Template
Templates in PyTemplates extend a base Template class and must define a template method.

To create a new template, start by creating a folder called **templates** in your app with an empty **\_\_init\_\_.py** file.

Here is an example of a simple template that we will place in a file called **my\_template.py**

```python
from pytemplates.pytemplates import Template
class MyTemplate(Template):
    def template(*args):
        template = \
            [{'html'},
                [{'head'},
                    [{'title'}, 'Hello World!'],
                ],
                [{'body'},
                    [{'div.container'}, "Hello, this is a test!"],
                ]
            ]
        return template
```
