from parser_gen.grammar_based import *


class myParser(Parser):
	@rule(Rule("dict"), out="S")
	def _(_1): return _1

	@rule('"', STRING, '"', out="string")
	def _(_1, v, _2):
		return v

	@rule(Rule("string"), ":", Rule("element"), out="kv")
	def _(k, _1, v):
		return k, v

	@rule("{", List(Rule("kv"), ","), "}", out="dict")
	def _(_1, l, _2):
		return {k:v for k,v in l}

	@rule("[", List(Rule("element"), ","), "]", out="list")
	def _(_1, l, _2):
		return l

	@rule(SCNUM, out="number")
	def _(_1):
		return eval(_1)
	@rule(FLOAT, out="number")
	def _(_1):
		return float(_1)
	@rule(NUM, out="number")
	def _(_1):
		return int(_1)

	@rule(Rule("number"), out="element")
	def _(_1): return _1
	@rule(Rule("string"), out="element")
	def _(_1): return _1
	@rule(Rule("dict"), out="element")
	def _(_1): return _1
	@rule(Rule("list"), out="element")
	def _(_1): return _1
	@rule("true", out="element")
	def _(_1): return True
	@rule("false", out="element")
	def _(_1): return False


if __name__ == "__main__":
	with open("test.json", "r") as f:
		t = f.read()
	p = myParser(t, verbose=False)
	while True:
		result = p.parse()
		if result is TokenNotFound:
			break
		print(result)
		input(p.index)
