from parser_gen.template_based import *


with open("template.txt", "r") as f:
	parser = Parser(f.read())

with open("text.txt", "r") as f:
	output = parser.parse(f.read(), collapse=True, evaluate=True)
print(output)
