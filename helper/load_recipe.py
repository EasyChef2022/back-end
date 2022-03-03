import csv
import psycopg2

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


def load_recipe():
    conn = get_conn()
    cur = conn.cursor()

    with open('../recipe_file/all_recipe.csv', 'r') as recipe_file:
        reader = csv.DictReader(recipe_file)
        for line in reader:
            pass


if __name__ == '__main__':
    # con = get_conn()
    load_recipe()
