# from dbmanager import DBManager
import dbmanager
from rich.console import Console
from rich.table import Table

class Insight:

    MENU = {
        "1" : {
            "title": "List of restaurants",
            "description": "List of restaurants included in the research filter by[''| category=string | city=string]",
            "method": "list_restaurants"
        },
        "2" : {
            "title": "List of dishes",
            "description": "List of unique dishes included in the research",
            "method": "list_dishes"
        },
        "3" : {
            "title": "Number and distribution of clients",
            "description": "Number and distribution (%) of clients by [group=[age | gender | occupation | nationality]]",
            "method": "distribution_clients_by"
        },
        "4" : {
            "title": "Top 10 restaurants by visitors",
            "description": "Top 10 restaurants by the number of visitors.",
            "method": "top_by_visitors"
        },
        "5" : {
            "title": "Top 10 restaurants by sales",
            "description": "Top 10 restaurants by the sum of sales.",
            "method": "top_by_sales"
        },
        "6" : {
            "title": "Top 10 restaurants by average expense per user",
            "description": "Top 10 restaurants by the average expense of their clients.",
            "method": "top_by_average_expense_user"
        },
        "7" : {
            "title": " Average consumer expenses",
            "description": "The average consumer expense group by [group=[age | gender | occupation | nationality]]",
            "method": "average_consumer_expenses_by"
        },
        "8" : {
            "title": "Total sales by month",
            "description": "The total sales of all the restaurants group by month [order=[asc | desc]]",
            "method": "total_sales"
        },
        "9" : {
            "title": "Best price for dish",
            "description": "The list of dishes and the restaurant where you can find it at a lower price",
            "method": "price_by_dish"
        },
        "10" : {
            "title": "Favorite dish",
            "description": "The favorite dish for [age=number | gender=string | occupation=string | nationality=string]",
            "method": "find_favourite_dish_by"
        },
        "11" : {
            "title" : "Insert a new visit to list",
            "description": "A new visit",
            "method": "insert_a_new_visit"
        },
        "12" : {
            "title" : "Top last ten models",
            "description": "Show the last ten models",
            "method" : "top_last_ten_models"
        }
    }
    

    def __init__(self):
        self.m_dbmanager = dbmanager.DBManager()

    def print_welcome(self):
        print("\t\t Welcome to the Restaurants Insights!")
        print("\t\t Write 'menu' at any moment to print the menu again and 'quit' to exit.")


    def print_menu(self):
        print(" \
                ---\n \
                1. List of restaurants included in the research filter by[''| category=string | city=string]\n \
                2. List of unique dishes included in the research\n \
                3. Number and distribution (%) of clients by [group=[age | gender | occupation | nationality]]\n \
                4. Top 10 restaurants by the number of visitors.\n \
                5. Top 10 restaurants by the sum of sales.\n \
                6. Top 10 restaurants by the average expense of their clients.\n \
                7. The average consumer expense group by [group=[age | gender | occupation | nationality]]\n \
                8. The total sales of all the restaurants group by month [order=[asc | desc]]\n \
                9. The list of dishes and the restaurant where you can find it at a lower price.\n \
                10. The favorite dish for [age=number | gender=string | occupation=string | nationality=string]\n \
                11. Insert a new dataset to list \n \
                12. Show the last ten models \n \
                ---\n \
                Pick a number from the list and an [option] if neccesary\n"
        )
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
            #print(res)
            self.print_table(res, action)
    
    def print_table(self, res, action):
        table = Table(title= self.MENU[action]["title"])

        for key in res[0]:
            table.add_column(key, justify="right", style="cyan", no_wrap=True)
        
        for i in range(0, len(res)):
            row = []
            for key in res[i]:
                row.append(str(res[i][key]))
            table.add_row(*row)
        console = Console()
        console.print(table)

insight = Insight()
insight.start()