import csv 
import psycopg2
import re
import sys 

filename = sys.argv[1]

DB_connect = psycopg2.connect(dbname='insights_python')
DB = DB_connect.cursor()


def take_client_data (row):
    return {
        "name" : row["client_name"],
        "age" : row["age"],
        "gender" : row ["gender"],
        "occupation" : row["occupation"],
        "nationality" : row["nationality"]
    }


def create(table, data):
    values = []
    for value in data.values():
        values.append("'" + re.sub("'", "''", value) + "'")

    query = f"INSERT INTO {table} ({','.join(data.keys())}) VALUES ({','.join(values)}) RETURNING *;"
    print(query)
    DB.execute(query)
    DB.fetchone()

def find (table,column, value):
    value = "'" + re.sub("'", "''", value) + "'"
    DB.execute(f"SELECT * from {table} where {column} = {value};")
    DB.fetchone()

def find_or_create (table, column, data):
    return find(table, column, data[column]) or create(table, data)


with open('data.csv', newline='') as File:  
    reader = csv.DictReader(File)
    for row in reader:
        client_data = take_client_data(row)
        client = find_or_create("clients", "name", client_data)


