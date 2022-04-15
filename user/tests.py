import sys

from django.test import TestCase, SimpleTestCase
from django.conf import settings
import requests
import random
import string


def Random_String(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))


class UserTest(TestCase):
    def setUp(self):
        self.baseurl = 'http://127.0.0.1:8000/user/'

    def test_user_sign_up(self):
        response = requests.post(self.baseurl + 'sign_up',
                                 json={'username': Random_String(8), 'password': Random_String(8)})
        self.assertEqual(response.status_code, 200)

    def test_duplicate_user(self):
        username = Random_String(10)
        password = Random_String(10)
        response = requests.post(self.baseurl + 'sign_up',
                                 json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)
        response = requests.post(self.baseurl + 'sign_up',
                                 json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 400)

    def test_user_sign_in(self):
        username = Random_String(10)
        password = Random_String(10)
        response = requests.post(self.baseurl + 'sign_up',
                                 json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)
        response = requests.post(self.baseurl + 'sign_in', json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_username(self):
        username = Random_String(10)
        password = Random_String(10)
        response = requests.post(self.baseurl + 'sign_up',
                                 json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)
        response = requests.get(self.baseurl + 'get_user?username=' + username)
        self.assertEqual(response.status_code, 200)

    def test_add_pantry_herb(self):
        username = Random_String(10)
        password = Random_String(10)
        response = requests.post(self.baseurl + 'sign_up',
                                 json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)
        response = requests.post(self.baseurl + 'sign_in', json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)
        token = response.json()['token']

        response = requests.post(self.baseurl + 'add_pantry', json={"username": username,
                                                                    "item": "a Kind of herb",
                                                                    "type": "herbs"},
                                 headers={'Authorization': 'Bearer ' + token})

        self.assertEqual(response.status_code, 200)
        response = requests.get(self.baseurl + 'get_user?username=' + username)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user']['herbs'][0], 'a Kind of herb')

    def test_add_pantry_spice(self):
        username = Random_String(10)
        password = Random_String(10)
        response = requests.post(self.baseurl + 'sign_up',
                                 json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)
        response = requests.post(self.baseurl + 'sign_in', json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)
        token = response.json()['token']

        response = requests.post(self.baseurl + 'add_pantry', json={"username": username,
                                                                    "item": "a Kind of spices",
                                                                    "type": "spices"},
                                 headers={'Authorization': 'Bearer ' + token})

        self.assertEqual(response.status_code, 200)
        response = requests.get(self.baseurl + 'get_user?username=' + username)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user']['spices'][0], 'a Kind of spices')

    def test_delete_pantry(self):
        username = Random_String(10)
        password = Random_String(10)
        response = requests.post(self.baseurl + 'sign_up',
                                 json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)
        response = requests.post(self.baseurl + 'sign_in', json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)
        token = response.json()['token']

        response = requests.post(self.baseurl + 'add_pantry', json={"username": username,
                                                                    "item": "a Kind of herb",
                                                                    "type": "herbs"},
                                 headers={'Authorization': 'Bearer ' + token})

        self.assertEqual(response.status_code, 200)
        response = requests.get(self.baseurl + 'get_user?username=' + username)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user']['herbs'][0], 'a Kind of herb')

        response = requests.post(self.baseurl + 'remove_pantry', json={"username": username,
                                                                       "item": "a Kind of herb",
                                                                       "type": "herbs"},
                                 headers={'Authorization': 'Bearer ' + token})
        self.assertEqual(response.status_code, 200)
        response = requests.get(self.baseurl + 'get_user?username=' + username)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['user']['herbs']), 0)
