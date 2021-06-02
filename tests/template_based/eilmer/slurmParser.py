from parser_gen.template_based import *
from pprint import pprint


with open("slurm-template.txt", "r") as f:
	parser = Parser(f.read())


for fname in ("slurm-1.out", "slurm-2.out"):
	with open(fname, "r") as f:
		output = parser.parse(f.read(), collapse=True, evaluate=True)
	pprint(output)
