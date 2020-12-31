import psycopg2.extras
from rich.console import Console
from rich.table import Table
from datetime import date
import datetime
import re
#import client as cl
from client import Client

console = Console() 

class DBManager:
    
    def __init__(self):
        self.DB_connect = psycopg2.connect(dbname='insights_python')
        self.DB = self.DB_connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        
    def list_restaurants(self, parameter=None):
        query = ""
        if parameter== None:
            query = "SELECT name, category, city FROM restaurants"
        else:
            print(parameter)
            column, value = parameter.split("=")   
            print(column, value) 
            query = f"SELECT name, category, city FROM restaurants WHERE LOWER ({column}) LIKE LOWER ('{value}')"
        self.DB.execute(query)
        return self.DB.fetchall()      
      
    def list_dishes(self):
        query = "SELECT name FROM dishes"
        self.DB.execute(query)
        return self.DB.fetchall() 

    def distribution_clients_by(self, parameter):
        _column, value = parameter.split("=")

        query = f"SELECT {value}, COUNT({value}) AS count, \
        CONCAT(ROUND(count({value})*100.00/499.00), '%') AS percentage\
        FROM clients\
        GROUP BY {value} ORDER BY {value};"
        self.DB.execute(query)
        return self.DB.fetchall()

    def top_by_visitors(self):
        query = "SELECT DISTINCT restaurants.name as name,\
        COUNT(visits.visit_date) as visitors\
        FROM visits\
        JOIN dishes_restaurants\
        ON visits.dishes_restaurants_id = dishes_restaurants.id\
        JOIN restaurants\
        ON dishes_restaurants.restaurant_id = restaurants.id\
        GROUP BY restaurants.name\
        ORDER BY visitors DESC LIMIT 10;"
        self.DB.execute(query)
        return self.DB.fetchall()
    

    def top_by_sales(self):
        query = f"SELECT name, sum(price_dish) as sales FROM (\
            SELECT v.visit_date, r.name, dr.price_dish FROM restaurants as r\
            JOIN dishes_restaurants as dr ON dr.restaurant_id=r.id\
            JOIN visits as v ON v.dishes_restaurants_id=dr.id\
            )as tmp\
            GROUP BY name\
            ORDER BY sales desc LIMIT 10;"
        self.DB.execute(query)
        return self.DB.fetchall()

    def top_by_average_expense_user(self):
        query = f"SELECT name, cast(avg(price_dish) as decimal(3,1)) as avg_expense FROM (\
            SELECT v.visit_date, r.name, dr.price_dish FROM restaurants as r\
            JOIN dishes_restaurants as dr ON dr.restaurant_id=r.id\
            JOIN visits as v ON v.dishes_restaurants_id=dr.id\
        ) as tmp\
        GROUP BY name\
        ORDER BY avg_expense desc LIMIT 10;"
        self.DB.execute(query)
        return self.DB.fetchall()

    def average_consumer_expenses_by(self, parameter):
        _column, value = parameter.split("=")
        query = f"SELECT DISTINCT clients.{value} AS {value},\
        ROUND(AVG(dishes_restaurants.price_dish),2) AS \"avg expense\"\
        FROM visits\
        JOIN dishes_restaurants\
        ON visits.dishes_restaurants_id = dishes_restaurants.id\
        JOIN clients\
        ON visits.client_id = clients.id\
        GROUP BY {value};"
        self.DB.execute(query)
        return self.DB.fetchall()
    
    def total_sales(self, parameter):
        _column, value = parameter.split("=")

        query = f"SELECT\
        to_char(v.visit_date, 'month') AS month,\
        sum(dr.price_dish) AS total\
        from visits v inner join dishes_restaurants dr on v.dishes_restaurants_id = dr.id\
        GROUP BY 1 ORDER BY sum(dr.price_dish) {value};"

        self.DB.execute(query)
        return self.DB.fetchall()

    # def price_by_dish(); end

    # def find_favourite_dish_by(); end
    def model_manager(self,model):
        while True:
            model.print_menu()
            opt = input("Choose an option: ")
            if opt=="1":
                while True:
                    model.fill_fields()
                    if model.find():
                        attempting = input("This model already exist. Do you want to try again? Y/N")
                        if attempting == "N":
                            break
                    else:
                        try:
                            model_data = model.create()
                        except ValueError:
                            print("An  Error has ocurred in the client creation")
                        break 
                model_id = model["id"]
                break
            if opt=="2":
                model_data = model.valid()
                break
            else:
                print("Select a valid option")
        return model_data # model_id 

    def top_last_ten_models(self):
        while True:
            print("1.- Clients")
            print("2.- Restaurants")
            print("3.- Dishes")
            print("4.- Dishes-Resturant")
            print("5.- Visits")
            opt = input("Choose a model:")
            if opt in ["1","2","3","4","5"]:
                break
            else:
                print("No seas pendex :p")
        MODEL = {
            "1": 'clients',
            "2": 'restaurants',
            "3": 'dishes',
            "4": 'dishes_restaurants',
            "5": 'visits'
        }
        self.DB.execute(f"SELECT * FROM (SELECT * FROM {MODEL[opt]} ORDER BY id DESC LIMIT 10) as tmp ORDER BY id;")
        return self.DB.fetchall()

    def insert_a_new_visit(self):

        # visit_date = str(input('Enter the visit date (e.g 2019-03-09): '))
        visit_date = "'2020-03-09'"
        
        # Client Section
        client = Client()
        client_data = self.model_manager(client)
        print("client: ", client_data)
        return [client_data]
        # Restaurant Section
        #restaurant_id = self.restaurant_manager()

        # visit_date_obj = datetime.datetime.strptime(visit_date, '%Y-%m-%d')
        # visit_date_obj = visit_date_obj.date()
        # print(type(visit_date_obj))

        # query = f"INSERT INTO visits(visit_date) VALUES({visit_date});"
        # self.DB.execute(query)
        # self.DB_connect.commit()

        # client_name = input('Client name: ')
        # query = f"INSERT INTO clients(name) VALUES({client_name});"
        # self.DB.execute(query)

        # age = input('Age: ')
        # query = f"INSERT INTO clients(age) VALUES({age});"
        # self.DB.execute(query)

        # gender = input('Gender Male/Female: ')
        # query = f"INSERT INTO clients(gender) VALUES({gender});"
        # self.DB.execute(query)

        # occupation = input('Occupation: ')
        # query = f"INSERT INTO clients(occupation) VALUES({occupation});"
        # self.DB.execute(query)

        # nationality = input('Nationality: ')
        # query = f"INSERT INTO clients(nationality) VALUES({nationality});"
        # self.DB.execute(query)

        # restaurant_name = input('Restaurant name: ')
        # query = f"INSERT INTO restaurants(name) VALUES({restaurant_name});"
        # self.DB.execute(query)

        # restaurant_category = input('Category of the restaurant: ')
        # query = f"INSERT INTO restaurants(category) VALUES({restaurant_category})"
        # self.DB.execute(query)

        # city = input('City where It is located: ')
        # query = f"INSERT INTO restaurants(city) VALUES({city});"
        # self.DB.execute(query)

        # address = input('Address: ')
        # query = f"INSERT INTO restaurants(address) VALUES({address});"
        # self.DB.execute(query)

        # dish = input('Dish: ')
        # query = f"INSERT INTO dishes(name) VALUES({dish});"
        # self.DB.execute(query)

        # price = input('Price of the dish in dollars (e.g 17): ')
        # query = f"INSERT INTO dishes_restaurants(price_dish) VALUES({price});"
        # self.DB.execute(query)
    # def top_last_ten_visitors(self):
    #     query = f"SELECT "
    #     return "Data are inserted"
        

""" Q&A 

  1. What if we add a new client with the same fields to another existent client, the id would be different?
    Even when we have the same fields, the data is added, and we have a different id
    
    To remove the last element:
    delete from dishes where id=(select max(id) from dishes) returning *; 





"""