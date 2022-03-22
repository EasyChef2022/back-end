import csv
import json

import psycopg2
import requests
from psycopg2 import extras
from deprecated import deprecated

db_name = 'easychef'
db_user = 'postgres'
db_password = 'Karlhe459!'
db_host = 'localhost'
dp_port = '5432'


def get_conn():
    try:
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=dp_port)
        return conn
    except:
        print("Failed to connect to database")


def get_recipe_count():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM recipe')
    count = cur.fetchone()
    conn.close()
    return count[0]


def get_recipes(offset, limit):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM recipe order by id desc limit {limit} offset {offset}')
    recipes = cur.fetchall()
    conn.close()
    return recipes


def send_request():
    url = 'http://easychef.herokuapp.com/recipe/add_recipe'
    # url = 'http://localhost:8000/recipe/add_recipe'
    count = get_recipe_count()
    for i in range(0, count, 500):
        recipes = get_recipes(i, 500)
        data = {'recipes': recipes}
        # print(data)
        response = requests.post(url, data=json.dumps(data))
        print(response)


if __name__ == '__main__':
    send_request()
