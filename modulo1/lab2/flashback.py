# from dbmanager import DBManager
import dbmanager
from rich.console import Console
from rich.table import Table

# createdb insights_python
# psql insights_python < create.sql
# conda activate lab2
# python insert_data.py data.csv
# pip-compile requirements.in
# pip-sync requirements.txt
# psql -d flashback
# \dt
# \d commands;
# dropdb flashback

class Flashback:

    MENU = {
        "1" : {
            "title": "Commands",
            "description": "commands",
            "method": "crud_commands"
        },
        "2" : { 
            "title" : "English",
            "description" : "English language",
            "method" : "crud_english"
        },
        "3" : { 
            "title" : "Ideas",
            "description": "This option is to insert data to some english tables",
            "method": "crud_ideas"
        }
    }
    

    def __init__(self):
        self.m_dbmanager = dbmanager.DBManager()

    def print_welcome(self):
        print("")
        print("\t\t Welcome to the Flashback Insights!")
        print("\t\t Write 'menu' at any moment to print the menu again and 'quit' to exit.")

    def print_menu(self):
        print ("")
        for key in self.MENU:
            print(f"\t\t {key}.-"+self.MENU[key]["title"])
        print("\t\t Pick a number from the list and an [option] if neccesary\n")
        print ("\t\t Menu|Quit")
    
    def start(self):
        self.print_welcome()
        self.print_menu()
        
        while True:
            line=input("> ") 
            elements = line.split(None, 1) # "1" option separate 2 elements as maximum
            action, parameter = elements if len(elements)>1 else [elements[0],None]
            print("action: ", action)
            if line.lower()=="menu": self.print_menu()
            if line.lower()=="quit": exit(1)
            else: self.run_query(action, parameter)
            self.print_menu()
            
    def run_query(self, action, parameter=0):
        if action in list(self.MENU.keys()):
            method = self.MENU[action]["method"]
            print("method: ", method)
            if parameter:
                res = getattr(self.m_dbmanager, method)(parameter)
            else:
                res = getattr(self.m_dbmanager, method)()
                print(res)
            self.print_table(res, action)
    
    def print_table(self, res, action):
        table = Table(title= self.MENU[action]["title"])
        if res==[]:
            print("Res does not exists")
        else:
            for key in res[0]:
                #table.add_column(key, justify="right", style="cyan", no_wrap=True)
                table.add_column(key, style="cyan", no_wrap=True)        
            for i in range(0, len(res)):
                row = []
                for key in res[i]:
                    row.append(str(res[i][key]))
                table.add_row(*row)
            console = Console()
            console.print(table)
            
flashback = Flashback()
flashback.start()