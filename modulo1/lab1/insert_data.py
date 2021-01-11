import csv 
import psycopg2.extras
import re
import sys 

filename = sys.argv[1]
DB_connect = psycopg2.connect(dbname='insights_python')
DB = DB_connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

def take_client_data (row):
    return {
        "name" : row["client_name"],
        "age" : row["age"],
        "gender" : row ["gender"],
        "occupation" : row["occupation"],
        "nationality" : row["nationality"]
    }

def take_restaurant_data(row) :
    return {
    "name": row["restaurant_name"],
    "category": row["category"],
    "city": row["city"],
    "address": row["address"]
  }

def take_dish_data(row) : 
    return {
    "name": row["dish"]
  }

def take_dish_restaurant_data(row, restaurant, dish) :
    return {
    "price_dish": row["price"],
    "dish_id": str(dish['id']),
    "restaurant_id": str(restaurant['id'])
  }

def take_visit_data(row, client, dish_restaurant) :
    return {
    "visit_date": row["visit_date"],
    "client_id": str(client['id']),
    "dishes_restaurants_id": str(dish_restaurant['id'])
  }

def create(table, data):
    values = []
    for value in data.values():
        values.append("'" + re.sub("'", "''", value) + "'")

    query = f"INSERT INTO {table} ({','.join(data.keys())}) VALUES ({','.join(values)}) RETURNING *;"
    print(query)
    DB.execute(query)
    DB_connect.commit()
    return DB.fetchone()

def find (table,column, value):
    value = "'" + re.sub("'", "''", value) + "'"
    DB.execute(f"SELECT * from {table} where {column} = {value};")
    return DB.fetchone()
    
def find_or_create (table, column, data):
    element = find(table, column, data[column])
    if element == None: 
        return create(table, data)
    else:
        return element

with open(filename, newline='') as File:  
    reader = csv.DictReader(File)
    for row in reader:
        client_data = take_client_data(row)
        client = find_or_create("clients", "name", client_data)
        
        restaurant_data = take_restaurant_data(row)
        restaurant = find_or_create("restaurants", "name", restaurant_data)

        dish_data = take_dish_data(row)
        dish = find_or_create("dishes", "name", dish_data)

        dish_restaurant_data = take_dish_restaurant_data(row, restaurant, dish)
        dish_restaurant = create("dishes_restaurants", dish_restaurant_data)
 
        visits_data = take_visit_data(row, client, dish_restaurant)
        create("visits", visits_data)


