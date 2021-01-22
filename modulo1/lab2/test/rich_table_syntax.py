from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table

my_code = '''
def iter_first_last(values: Iterable[T]) -> Iterable[Tuple['bool', bool, T]]:
    iter_values = iter(values)
'''
my_code = "def foo()\n\tprint(sth)\n\tcalculate_function()\nend"
syntax = Syntax(my_code, "python", theme="monokai", line_numbers=True)
console = Console()
console.print(syntax)


table = Table(title= "test")

res = [{
  "category": "rails",
  "commandline": my_code,
  "description": "this is a .."
}]
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

# map
# filter
