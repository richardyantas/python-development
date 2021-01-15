import psycopg2.extras
from rich.console import Console
from rich.table import Table

console = Console()

class DBManager:
    
    def __init__(self):
        self.DB_connect = psycopg2.connect(dbname='flashback')
        self.DB = self.DB_connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        
    def find_or_create(self, data):
        query = f"SELECT * FROM commands WHERE commandline LIKE '{data['commandline']}';"
        self.DB.execute(query)
        if self.DB.fetchone():
            return self.DB.fetchall()
        else:
            #query = f"INSERT INTO commands(category, commandline, description) VALUES('{data['category']}', '{data['commandline']}', '{data['description']}') RETURNING *;"
            query = f"INSERT INTO commands(category, commandline, description) VALUES(LOWER('{data['category']}'), '{data['commandline']}', '{data['description']}'); SELECT * FROM commands WHERE category LIKE LOWER('{data['category']}');"
            self.DB.execute(query)
            self.DB_connect.commit()
            return self.DB.fetchall()
             
        
    def list_ruby_ror(self, parameter=None):        
        # ALTER TABLE commands ALTER COLUMN commandline TYPE varchar(100);
        # \d commands; \dt commands;
        # query = f"SELECT * FROM commands WHERE category LIKE '{data['category']}';"
        query = f"SELECT * FROM commands WHERE category LIKE 'rails';"
        self.DB.execute(query)
        return self.DB.fetchall()      

    def insert_ruby_ror(self,parameter=None):        
        print("Entering Ruby command data: ")
        #line = input("> ")
        data = {}
        data["category"] = input("> category: ")
        data["commandline"] = input("> commandline: ")
        data["description"] = input("> description: ")
        data = self.find_or_create(data)        
        return data

    def english_language_list(self, parameter=None): return
    def english_language_insert(self, parameter=None): return



