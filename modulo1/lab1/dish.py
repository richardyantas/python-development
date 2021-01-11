import psycopg2.extras
from rich.console import Console
from rich.table import Table
import re

class Dish:
    def __init__(self, name=""):
        self.DB_connect = psycopg2.connect(dbname='insights_python')
        self.DB = self.DB_connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        self.name = name
    
    def fill_fields(self):
        self.name = input("name: ")
    
    def create(self):
        data = {
                    "name": f"{self.name}"
        }
        values = []
        for value in data.values():
            values.append("'" + re.sub("'", "''", value) + "'")
        query = f"INSERT INTO dishes ({','.join(data.keys())}) VALUES ({','.join(values)}) RETURNING *;"
        print(query)
        self.DB.execute(query)
        self.DB_connect.commit()
        return self.DB.fetchone()
    
    def find(self):
        self.DB.execute(f"SELECT * from dishes where name='{self.name}';")
        return self.DB.fetchone()

    def valid(self):
        while True:
            self.name_entered = input("Enter a dish name: ")
            # data_row = self.find(self.name_entered)   
            self.DB.execute(f"SELECT * from dishes where name='{self.name_entered}';")   
            data_row = self.DB.fetchone()    
            if data_row == None:
                attempting = input("This dish does not exist. Do you want to try again? Y/N")
                if attempting == "N":
                    break
            else:
                break
        return data_row

    def print_menu(self):
        print("\t\t 1.- Add a new dish to visit")
        print("\t\t 2.- Add an existent dish to visit")