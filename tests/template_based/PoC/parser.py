from parser_gen.template_based import *
from pprint import pprint


with open("template.txt", "r") as f:
	template = f.read()
	parser = Parser(template)

with open("text.txt", "r") as f:
	content = f.read()
	output = parser.parse(content, collapse=True, evaluate=True)
pprint(output)
