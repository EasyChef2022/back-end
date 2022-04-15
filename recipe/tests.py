import sys

from django.test import TestCase, SimpleTestCase
from django.conf import settings
import requests


# Create your tests here.

class RecipeTest(TestCase):
    def setUp(self):
        self.baseurl = 'http://127.0.0.1:8000/recipe/'

    def test_recipe_of_today(self):
        results = []
        for i in range(10):
            response = requests.get(self.baseurl + 'get_recipe_of_today')
            self.assertEqual(response.status_code, 200)
            results.append(response.json()['id'])
        self.assertEqual(len(set(results)), 1)

    def test_get_recipe_by_id(self):
        id = requests.get(self.baseurl + 'get_recipe_of_today').json()['id']
        response = requests.get(self.baseurl + 'get_recipe_by_id?id=' + str(id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], id)

    def test_get_recipe_by_id_invalid(self):
        response = requests.get(self.baseurl + 'get_recipe_by_id?id=-1')
        self.assertEqual(response.status_code, 500)

    def test_get_recipe_by_exact_match(self):
        response = requests.post(self.baseurl + 'get_recipe_by_exact_match',
                                 json={'ingredients': ['butter'], 'ban': []})
        self.assertEqual(response.status_code, 200)

    def test_get_recipe_by_ingredients(self):
        response = requests.post(self.baseurl + 'get_recipe_by_ingredients',
                                 json={'ingredients': ['butter'], 'ban': []})
        self.assertEqual(response.status_code, 200)

    def test_sort_recipe_by_time(self):
        response = requests.post(self.baseurl + 'get_recipe_by_exact_match',
                                 json={'ingredients': ['butter'], 'ban': [], 'sort': 'time'})
        old = -1
        for i in response.json()['result']:
            assert (old <= i['cook_time'])
            old = i['cook_time']
        self.assertEqual(response.status_code, 200)

    def test_sort_recipe_by_complexity(self):
        response = requests.post(self.baseurl + 'get_recipe_by_exact_match',
                                 json={'ingredients': ['butter'], 'ban': [], 'sort': 'complexity'})
        old = -1
        for i in response.json()['result']:
            assert (old <= len(i['ingredients']))
            old = len(i['ingredients'])
        self.assertEqual(response.status_code, 200)

    def test_sort_recipe_by_rating(self):
        response = requests.post(self.baseurl + 'get_recipe_by_exact_match',
                                 json={'ingredients': ['butter'], 'ban': [], 'sort': 'rating'})
        old = sys.maxsize
        for i in response.json()['result']:
            assert (old >= i['rating'])
            old = i['rating']
        self.assertEqual(response.status_code, 200)

    def test_sort_recipe_by_default(self):
        response = requests.post(self.baseurl + 'get_recipe_by_exact_match',
                                 json={'ingredients': ['butter'], 'ban': [], 'sort': ''})
        old = sys.maxsize
        for i in response.json()['result']:
            assert (old >= i['rating'])
            old = i['rating']
        self.assertEqual(response.status_code, 200)

        response = requests.post(self.baseurl + 'get_recipe_by_exact_match',
                                 json={'ingredients': ['butter'], 'ban': [], 'sort': 'a'})
        old = sys.maxsize
        for i in response.json()['result']:
            assert (old >= i['rating'])
            old = i['rating']
        self.assertEqual(response.status_code, 200)

        response = requests.post(self.baseurl + 'get_recipe_by_exact_match',
                                 json={'ingredients': ['butter'], 'ban': []})
        old = sys.maxsize
        for i in response.json()['result']:
            assert (old >= i['rating'])
            old = i['rating']
        self.assertEqual(response.status_code, 200)
