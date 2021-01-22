import command
import requester
import presenter
import psycopg2.extras
from rich.console import Console
from rich.table import Table

console = Console()

class DBManager:

    def __init__(self):
        self.DB_connect = psycopg2.connect(dbname='flashback')
        self.DB = self.DB_connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
             
    def crud_commands(self, parameter=None):
        command_ = command.Command()
        presenter.print_menu(command_.MENU)
        option = input("> ")
        method = command_.MENU[option]["method"]
        # command_.create()
        # command_.update()
        # command_.delete()
        # command_.show()
        return getattr(command_, method)()


# python test/rich_table_syntax.py
