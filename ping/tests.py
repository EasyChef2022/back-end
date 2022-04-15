from django.test import TestCase
import requests


# Create your tests here.
class PingTest(TestCase):
    def setUp(self):
        self.baseurl = 'http://127.0.0.1:8000/'

    def test_ping(self):
        response = requests.get(self.baseurl + 'ping')
        self.assertEqual(response.status_code, 200)
