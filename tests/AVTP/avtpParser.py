from parser_gen.grammar_based import *


BLOB = Regex("[^ ]+")
class myParser(Parser):
	@rule("*****", "Solution stored in file:", BLOB, Rule("AVTP1"), Rule("AVTP2"), out="S")
	def _(_1, _2, fname, avtp1, avtp2):
		return Node("solution", fname=fname, avtp1=avtp1, avtp2=avtp2)

	@rule("AVTP", "timeit", "=", Rule("number"), out="AVTP1")
	def _(_1, _2, _3, v):
		return v

	@rule("AVTP", NUM, Rule("number"), Rule("number"), out="AVTP2")
	def _(_1, a, b, c):
		return a, b, c

	@rule(SCNUM, out="number")
	def _(_1):
		return _1
	@rule(FLOAT, out="number")
	def _(_1):
		return _1
	@rule(NUM, out="number")
	def _(_1):
		return _1


if __name__ == "__main__":
	with open("sub_avtp.out", "r") as f:
		t = f.read()
	p = myParser(t)
	result = True
	while result:
		result = p.parse()
		print(result)
		input()
