from __future__ import absolute_import

from pytemplates.pytemplates import Template
import unittest
from pytemplates.utils import render_content
from pytemplates.utils import render_empty_tag


class TestingTemplate(Template):
    def template(self, *args, **kwargs):
        out = [{'html'}]
        return out


class TestTemplate(unittest.TestCase):
    def setUp(self):
        self.template = TestingTemplate()

    def test_render_template(self):
        expected = "<!DOCTYPE html><html></html>"
        self.assertEqual(self.template.render(), expected)

    def test_render_empty_tag(self):
        tag = ({'input'})
        self.assertEqual(render_empty_tag(tag), '<input>')

    def test_render_content(self):
        content = [{'div'}, [{'h1'}, 'test']]
        self.assertEqual(render_content(*content), '<div><h1>test</h1></div>')

    def test_short_form(self):
        content1 = [{'a.c1.c2#test_id[href="#"][data-test="test"]:disabled'}, 'test']
        content2 = [{'a.c1.c2#test_id[href=\'#\'][data-test=\'test\']:disabled'}, 'test']
        rendered1 = render_content(*content1)
        rendered2 = render_content(*content2)
        expected = '<a data-test="test" class="c1 c2" id="test_id" href="#" disabled>test</a>'
        self.assertEqual(1, rendered1.count('<a'))
        self.assertEqual(1, rendered1.count('data-test="test"'))
        self.assertEqual(1, rendered1.count('class="c1 c2"'))
        self.assertEqual(1, rendered1.count('id="test_id"'))
        self.assertEqual(1, rendered1.count('href="#"'))
        self.assertEqual(1, rendered1.count('disabled'))
        self.assertEqual(1, rendered1.count('>test</a>'))

        self.assertEqual(1, rendered2.count('<a'))
        self.assertEqual(1, rendered2.count('data-test="test"'))
        self.assertEqual(1, rendered2.count('class="c1 c2"'))
        self.assertEqual(1, rendered2.count('id="test_id"'))
        self.assertEqual(1, rendered2.count('href="#"'))
        self.assertEqual(1, rendered2.count('disabled'))
        self.assertEqual(1, rendered2.count('>test</a>'))

    def test_long_form(self):
        content1 = [{'div', ('test1', 'test1'), ('test2',)}, 'test']
        expected = '<div test1="test1" test2>test</div>'
        self.assertEqual(render_content(*content1), expected)

    def test_nested_tags(self):
        content = [
            {'d1'},[
                {'d2'}, [
                    {'d3'}, 'test']]]
        expected = '<d1><d2><d3>test</d3></d2></d1>'
        self.assertEqual(render_content(*content), expected)

if __name__ == '__main__':
    unittest.main()
