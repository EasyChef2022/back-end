import csv
import psycopg2
from psycopg2 import extras

db_name = 'easychef'
db_user = 'postgres'
db_password = 'Karlhe459!'
db_host = 'localhost'
dp_port = '5432'


def str2arrfield(s):
    return '\'{' + s.replace('[', '').replace(']', '').replace("\'", "") + '}\''


def str2str(s):
    return '\'' + s.replace('[', '').replace(']', '').replace("\'", "") + '\''


def str2time(s):
    s = s.replace(" minutes", "")
    try:
        return int(s)
    except:
        return -1


def get_conn():
    try:
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=dp_port,
                                cursor_factory=extras.RealDictCursor)
        return conn
    except:
        print("Failed to connect to database")


def load_recipe():
    conn = get_conn()
    cur = conn.cursor()
    with open('../recipe_data/all_recipe.csv', 'r') as recipe_file:
        reader = csv.DictReader(recipe_file)
        for line in reader:
            cooking_method = str2arrfield(line['cooking_method'])
            cuisine = str2str(line['cuisine'])
            image = str2str(line['image'])
            ingredients = str2arrfield(line['ingredients'])
            name = str2str(line['recipe_name'])
            prep_time = str2time(line['prep_time'])
            tags = str2arrfield(line['tags'])
            sql = f'INSERT INTO recipe (cooking_method, cuisine, image, ingredients, name, prep_time, tags) VALUES ({cooking_method}, {cuisine}, {image}, {ingredients}, {name}, {prep_time}, {tags})'
            # print(sql)
            cur.execute(sql)
            conn.commit()
            print(cooking_method, cuisine, image, ingredients, name, prep_time, tags)
            break


def test_result():
    conn = get_conn()
    cur = conn.cursor()
    sql = 'SELECT * FROM recipe'
    cur.execute(sql)
    result = cur.fetchall()
    print(len(result))
    for row in result:
        print(row)
