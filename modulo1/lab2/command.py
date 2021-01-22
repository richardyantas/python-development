import psycopg2.extras
import requester
import presenter

class Command():
  COMMAND = {
      "1" : {
          "title": "rails",
          "description": "List Ruby commands",
      },
      "2" : {
          "title": "R",
          "description": "Top 10 restaurants by the number of visitors.",
      },
      "3" : {
          "title": "SQL",
          "description": "Top 10 restaurants by the sum of sales.",
      },
      "4" : {
          "title": "CMake",
          "description": "Top 10 restaurants by the average expense of their clients.",
      },
      "5" : {
          "title": "Docker",
          "description": "The average consumer expense group by [group=[age | gender | occupation | nationality]]",
      },
      "6" : {
          "title": "Git",
          "description": "The total sales of all the restaurants group by month [order=[asc | desc]]",
      },
      "7" : {
          "title": "Css/Html",
          "description": "The list of dishes and the restaurant where you can find it at a lower price",
      },
      "8" : {
          "title": "Javascript",
          "description": "The favorite dish for [age=number | gender=string | occupation=string | nationality=string]",
      },
      "9" : {
          "title" : "Python",
          "description": "A new visit",
      },
      "10" : {
          "title" : "C++",
          "description": "Show the last ten models",
      },
      "11" : {
          "title" : "linux",
          "description": "Show the last ten models",
      },
      "12" : {
          "title" : "conda",
          "description": "Show the last ten models",
      }
  }
  # CRUD operations
  MENU = {
      "1": {
        "title": "List",
        "method": "show"
      },
      "2": {
        "title": "Insert",
        "method": "create"
      },
      "3": {
        "title": "Update",
        "method": "update"
      },
      "4": {
        "title": "Delete",
        "method": "delete"
      }
  }

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

  def show(self, parameter=None):        
        presenter.print_menu(self.COMMAND)
        line=input("> ")
        # ALTER TABLE commands ALTER COLUMN commandline TYPE varchar(100);
        # \d commands; \dt commands;
        # query = f"SELECT * FROM commands WHERE category LIKE '{data['category']}';"
        query = f"SELECT * FROM commands WHERE category LIKE LOWER('{line}');"
        self.DB.execute(query)
        return self.DB.fetchall()

  def create(self,parameter=None):        
        print("Entering Ruby command data: ")
        data = {}
        data["category"] = input("> category: ")
        data["commandline"] = requester.input_paragraph("commandline: ")
        data["description"] = requester.input_paragraph("description: ")
        data = self.find_or_create(data)
        return data
