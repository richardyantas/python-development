

def input_paragraph(field):
	lines = []
	print("> " + field)
	while True:
		line = input("> ")
		if line:
			lines.append(line)
		else:
			break
	text = '\n'.join(lines)
	return text