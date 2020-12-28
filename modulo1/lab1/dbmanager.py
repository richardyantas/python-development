import psycopg2
from rich.console import Console
from rich.table import Table

console = Console() 

class DBManager:
    
    def __init__(self):
        self.db = psycopg2.connect(dbname: 'insights')
        
    def list_restaurants(*params):
        query = %()
        if params== None:
        query = %(SELECT name, category, city FROM restaurants)
        else
        column, value = params[0].split("=")
        query = %( SELECT name, category, city FROM restaurants
            WHERE LOWER\(#{column}\) LIKE LOWER\('#{value}'\))
        
        self.db.exec(query)
  

    def list_dishes(self):
        query = %(SELECT name FROM dishes)
        @db.exec(query)
    

    def distribution_clients_by(param):
        _column, value = param.split("=")

        query = %(SELECT #{value}, COUNT(#{value}) AS count, 
        CONCAT(ROUND(count(#{value})*100.00/499.00), '%') AS percentage
        FROM clients
        GROUP BY #{value} ORDER BY #{value};)

        @db.exec(query)
    

    def top_by_visitors():
        query = %(SELECT DISTINCT restaurants.name as name,
        COUNT(visits.visit_date) as visitors
        FROM visits
        JOIN dishes_restaurants
        ON visits.dishes_restaurants_id = dishes_restaurants.id
        JOIN restaurants
        ON dishes_restaurants.restaurant_id = restaurants.id
        GROUP BY restaurants.name
        ORDER BY visitors DESC LIMIT 10;)

        @db.exec(query)
    

