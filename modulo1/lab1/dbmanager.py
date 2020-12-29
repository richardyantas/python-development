#REVISAR CODIGO, NO SE SI ESTA BIEN O_O
import psycopg2.extras
from rich.console import Console
from rich.table import Table

console = Console() 

class DBManager:
    
    def __init__(self):
        self.DB_connect = psycopg2.connect(dbname='insights_python')
        self.DB = self.DB_connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        
    def list_restaurants(self, parameter=0):
        query = ""
        if parameter== None:
            query = "SELECT name, category, city FROM restaurants"
        else:
            print(parameter)
            column, value = parameter.split("=")   
            print(column, value) 
            query = f"SELECT name, category, city FROM restaurants WHERE LOWER ({column}) LIKE LOWER ('{value}')"
        #print(query)
        self.DB.execute(query)
        return self.DB.fetchall()      
      
    def list_dishes(self):
        query = "SELECT name FROM dishes"
        self.DB.execute(query)
        return self.DB.fetchall() 

    # def distribution_clients_by(self, param):
    #     _column, value = param.split("=")

    #     querP BY {value} ORDER BY {value};"

    #     self.db.execute(query)
    
#     def top_by_visitors(self):
#         query = "SELECT DISTINCT restaurants.name as name,\
#         COUNT(visits.visit_date) as visitors\
#         FROM visits\
#         JOIN dishes_restaurants\
#         ON visits.dishes_restaurants_id = dishes_restaurants.id\
#         JOIN restaurants\
#         ON dishes_restaurants.restaurant_id = restaurants.id\
#         GROUP BY restaurants.name\
#         ORDER BY visitors DESC LIMIT 10;"

#         self.db.execute(query)
    
# y = f"SELECT {value}, COUNT({value}) AS count,\
#         CONCAT(ROUND(count({value})*100.00/499.00), '%') AS percentage\
#         FROM clients\
#         GROUP BY {value} ORDER BY {value};"

#         self.db.execute(query)
    
#     def top_by_visitors(self):
#         query = "SELECT DISTINCT restaurants.name as name,\
#         COUNT(visits.visit_date) as visitors\
#         FROM visits\
#         JOIN dishes_restaurants\
#         ON visits.dishes_restaurants_id = dishes_restaurants.id\
#         JOIN restaurants\
#         ON dishes_restaurants.restaurant_id = restaurants.id\
#         GROUP BY restaurants.name\
#         ORDER BY visitors DESC LIMIT 10;"

#         self.db.execute(query)
    

