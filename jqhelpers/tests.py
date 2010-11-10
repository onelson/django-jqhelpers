from django.utils import unittest
from django.test.client import Client

def is_unique_list(seq):
    for i in seq:
        if seq.count(i) != 1:
            return False
    return True

class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        
        self.assertTrue(is_unique_list(response.context['jq_plugins']))
        self.assertTrue(is_unique_list(response.context['jq_scripts']))