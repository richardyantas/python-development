import psycopg2.extras
from rich.console import Console
from rich.table import Table
import re

class Restaurant:
    def __init__(self, name="",category="",city="",address=""):
        self.DB_connect = psycopg2.connect(dbname='insights_python')
        self.DB = self.DB_connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        self.name = name
        self.category = category
        self.city = city
        self.address = address
    
    def fill_fields(self):
        self.name = input("name: ")
        self.category = input("category: ")
        self.city = input("city: ")
        self.address = input("address: ")

        #return self.data
    
    def create(self):
        data = {
            "name": f"{self.name}",
            "category": f"{self.category}",
            "city": f"{self.city}",
            "address": f"{self.address}"
        }

        values = []
        for value in data.values():
            values.append("'" + re.sub("'", "''", value) + "'")
        query = f"INSERT INTO restaurants ({','.join(data.keys())}) VALUES ({','.join(values)}) RETURNING *;"
        print(query)
        self.DB.execute(query)
        self.DB_connect.commit()
        return self.DB.fetchone()
    
    def find(self):
        self.DB.execute(f"SELECT * from restaurants where name='{self.name}';")
        return self.DB.fetchone()

    def valid(self):
        while True:
            self.name_entered = input("Enter a restaurant name: ")
            self.DB.execute(f"SELECT * from dishes_restaurants where name='{self.name_entered}';")
            data_row = self.DB.fetchone()           
            if data_row == None:
                attempting = input("This restaurant does not exist. Do you want to try again? Y/N")
                if attempting == "N":
                    break
            else:
                break
        return data_row

    def print_menu(self):
        print("\t\t 1.- Add a new restaurant to visit")
        print("\t\t 2.- Add an existent restaurant to visit")