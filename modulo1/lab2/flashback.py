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
            "title": "List of Ruby/Rails Commands",
            "description": "List of restaurants included in the research filter by[''| category=string | city=string]",
            "method": "list_ruby_ror"
        },
        "2" : {
            "title": "Insert of Ruby/Rails Commands",
            "description": "Insert of Ruby/Rails Commands for development and good practices",
            "method": "insert_ruby_ror"
        },
        "3" : {
            "title": "List of Linux Commands",
            "description": "Number and distribution (%) of clients by [group=[age | gender | occupation | nationality]]",
            "method": "distribution_clients_by"
        },
        "4" : {
            "title": "List of R commands",
            "description": "Top 10 restaurants by the number of visitors.",
            "method": "top_by_visitors"
        },
        "5" : {
            "title": "List of SQL commands",
            "description": "Top 10 restaurants by the sum of sales.",
            "method": "top_by_sales"
        },
        "6" : {
            "title": "List of CMake commands",
            "description": "Top 10 restaurants by the average expense of their clients.",
            "method": "top_by_average_expense_user"
        },
        "7" : {
            "title": "List of Docker commands",
            "description": "The average consumer expense group by [group=[age | gender | occupation | nationality]]",
            "method": "average_consumer_expenses_by"
        },
        "8" : {
            "title": "List of Git commands",
            "description": "The total sales of all the restaurants group by month [order=[asc | desc]]",
            "method": "total_sales"
        },
        "9" : {
            "title": "List of Css/Html commands",
            "description": "The list of dishes and the restaurant where you can find it at a lower price",
            "method": "price_by_dish"
        },
        "10" : {
            "title": "List of Javascript commands",
            "description": "The favorite dish for [age=number | gender=string | occupation=string | nationality=string]",
            "method": "find_favourite_dish_by"
        },
        "11" : {
            "title" : "List of Python/Conda Commands",
            "description": "A new visit",
            "method": "insert_a_new_visit"
        },
        "12" : {
            "title" : "List of C++ commands",
            "description": "Show the last ten models",
            "method" : "top_last_ten_models"
        },
        "13" : { 
            "title" : "List English",
            "description" : "Show strutures for the English language",
            "method" : "english_language_list"
        },
        "14" : { 
            "title" : "Insert English",
            "description": "This option is to insert data to some english tables",
            "method": "english_language_insert"
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
        for i in ["1","2","3","4","5","6","7","8","9"]:
            print(f"\t\t {i}.-"+self.MENU[i]["title"])
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
            if parameter:
                res = getattr(self.m_dbmanager, method)(parameter)
            else:
                res = getattr(self.m_dbmanager, method)()
            print("res: ", res)
            self.print_table(res, action)
    
    def print_table(self, res, action):
        table = Table(title= self.MENU[action]["title"])
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