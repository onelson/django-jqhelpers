from django.utils import unittest
from django.test.client import Client
from jqhelpers.templatetags.jq_tags import PLUGIN_CONTEXT_KEY, \
 SCRIPT_CONTEXT_KEY, SCRIPT_INLINE_CONTEXT_KEY


def is_unique_list(seq):
    for i in seq:
        if seq.count(i) != 1:
            return False
    return True


class RenderDemoTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        self.context_keys = [PLUGIN_CONTEXT_KEY,
                             SCRIPT_CONTEXT_KEY,
                             SCRIPT_INLINE_CONTEXT_KEY]

    def test_unique_context_content(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        for key in self.context_keys:
            self.assertTrue(is_unique_list(response.context[key]))
