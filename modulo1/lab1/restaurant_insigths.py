# from dbmanager import DBManager
import dbmanager

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
                ---\n \
                Pick a number from the list and an [option] if neccesary\n"
        )
    
    def start(self):
        self.print_welcome()
        self.print_menu()
        
        while True:
            line=input("> ")
            action, parameter = line.split(" ", 1)
            if line=="menu": self.print_menu()
            if line=="quit": exit(1)
            else: self.run_query(action, parameter)
            self.print_menu()
            
    def run_query(self, action, parameter=0):
        if action in list(self.MENU.keys()):
            method = self.MENU[action]["method"]
            if parameter:
                params =  [method, parameter]
            else:
                params = [method]
            print(params)
            # res = dbmanager.send(params)
            # print(res) # in table format  

        
    def foo(self):
        return self.m_dbmanager.db

insight = Insight()
print(insight.start())a