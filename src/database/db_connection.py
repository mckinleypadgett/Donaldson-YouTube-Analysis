import psycopg2
from psycopg2 import sql
from decouple import config

db_host = config('DATABASE_URL')
db_name = config('DATABASE_NAME')
db_user = config('DATABASE_USER')
db_pass = config('DATABASE_PASSWORD')
conn = ""
cursor = ""

def connect_db():
    #conn_string = "host={} dbname={} user={} password={}".format(db_host, db_name, db_user, db_pass)
    #conn = psycopg2.connect(conn_string)
    try:
        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_pass)
        print('Connection Successful')
    except:
        print('Connection Unsuccessful')

connect_db()