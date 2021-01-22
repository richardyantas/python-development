
def print_menu(menu):
	print ("")
	for key in menu:
		print(f"\t\t {key}.-" + menu[key]["title"])
	print("\t\t Pick a number from the list and an [option] if neccesary\n")
	print ("\t\t Menu|Quit")