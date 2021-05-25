from parser_gen.grammar_based import *
from avtpHeaderParser import headerParser


BLOB = Regex("[^ ]+")
class coreParser(Parser):
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

	def skip(self):
		index = self.text[self.index:].index('\n')
		if index == -1:
			self.eof()
			return False
		self.index += index+1
		return True


if __name__ == "__main__":
	with open("avtp.out", "r") as f:
		t = f.read()
	p = coreParser(t, verbose=False)
	p.add_rules(headerParser)
	while True:
		result = p.parse()
		if result is False:
			if p.head() is None:
				break
			p.skip()
		else:
			print(result)
			print(result.to_dict())
			input(p.index)
