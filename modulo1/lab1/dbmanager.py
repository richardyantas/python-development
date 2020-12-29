import psycopg2.extras
from rich.console import Console
from rich.table import Table

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

