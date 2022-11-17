import psycopg2
from psycopg2 import sql
from decouple import config

db_host = config('DATABASE_URL')
db_name = config('DATABASE_NAME')
db_user = config('DATABASE_USER')
db_pass = config('DATABASE_PASSWORD')


def connect_db():
    conn_string = "host={} dbname={} user={} password={}".format(db_host, db_name, db_user, db_pass)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('Connection Successful')
    
connect_db()