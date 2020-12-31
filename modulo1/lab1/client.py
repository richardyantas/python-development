import psycopg2.extras
from rich.console import Console
from rich.table import Table
from datetime import date
import datetime
import re

class Client:
    def __init__(self, name="",age=0,gender="",nationality="",occupation=""):
        self.DB_connect = psycopg2.connect(dbname='insights_python')
        self.DB = self.DB_connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        self.name = name
        self.age = age
        self.gender = gender
        self.nationality = nationality
        self.occupation = occupation
    
    def fill_fields(self):
        self.name = input("name: ")
        self.age = input("age: ")
        self.gender = input("gender: ")
        self.nationality = input("nationality: ")
        self.occupation = input("occupation: ")

    def create(self, data):
        values = []
        for value in data.values():
            values.append("'" + re.sub("'", "''", value) + "'")
        query = f"INSERT INTO clients ({','.join(data.keys())}) VALUES ({','.join(values)}) RETURNING *;"
        print(query)
        self.DB.execute(query)
        self.DB_connect.commit()
        return self.DB.fetchone()
    
    def find(self):
        self.DB.execute(f"SELECT * from clients where name='{self.name_entered}';")
        return self.DB.fetchone()

    def valid(self):
        while True:
            self.name_entered = input("Enter a client name: ")
            data_row = self.find()            
            if data_row == None:
                attempting = input("This client does not exist. Do you want to try again? Y/N")
                if attempting == "N":
                    break
            else:
                break
        return data_row

    def print_menu(self):
        print("\t\t 1.- Add a new client to visit")
        print("\t\t 2.- Add an existent client to visit")