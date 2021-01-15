    import psycopg2.extras
from rich.console import Console
from rich.table import Table
from datetime import date
import datetime
import re
from client import Client
from restaurant import Restaurant
from dish import Dish
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
                    #data = model.fill_fields()
                    model.fill_fields()
                    if model.find():
                        attempting = input("This model already exist. Do you want to try again? Y/N")
                        if attempting == "N":
                            break
                    else:
                        try:
                            model_data = model.create()
                        except ValueError:
                            print("An  Error has ocurred in the model creation")
                        break 
                model_id = model_data["id"]
                #model_id = model.id
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
        # Client Section
        client = Client()
        print(type(client))
        client_data = self.model_manager(client)
        print("client: ", client_data)

        # Restaurant Section
        restaurant = Restaurant()
        restaurant_data = self.model_manager(restaurant)
        print("restaurant: ", restaurant_data)
        #return [restaurant_data]

        # Dish Section
        dish = Dish()
        dish_data = self.model_manager(dish)
        print("dish: ", dish_data)
        #return [dish_data]

        #Dish_restaurant Section
        dish_data_id = dish_data["id"]
        restaurant_data_id = restaurant_data["id"]
        self.DB.execute(f"SELECT * from dishes_restaurants where dish_id='{dish_data_id}' AND restaurant_id='{restaurant_data_id}';")
        dish_restaurant_data = self.DB.fetchone() 
        if dish_restaurant_data == None:
            price_data = input("price: ")
            query = f"INSERT INTO dishes_restaurants (dish_id, restaurant_id, price_dish) VALUES ({dish_data_id}, {restaurant_data_id}, {price_data}) RETURNING *;"
            self.DB.execute(query)
            self.DB_connect.commit()
            dish_restaurant_data = self.DB.fetchone()

        #Visits Section
        dish_restaurant_id = dish_restaurant_data["id"]
        client_id = client_data["id"]
        self.DB.execute(f"SELECT * from visits where dishes_restaurants_id='{dish_restaurant_id}' AND client_id='{client_id}';")
        visit_data = self.DB.fetchone()
        if visit_data == None:
            visit_date = str(input('Enter the visit date (e.g 2019-03-09): '))
            query = f"INSERT INTO visits (dishes_restaurants_id, client_id, visit_date) VALUES ({dish_restaurant_id}, {client_id}, '{visit_date}') RETURNING *;"
            self.DB.execute(query)
            self.DB_connect.commit()
            visit_data = self.DB.fetchone()
        return [visit_data]

""" Q&A 

  1. What if we add a new client with the same fields to another existent client, the id would be different?
    Even when we have the same fields, the data is added, and we have a different id
    
    To remove the last element:
    delete from dishes where id=(select max(id) from dishes) returning *; 





"""