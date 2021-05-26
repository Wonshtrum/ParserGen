from parser_gen.grammar_based import *


class myParser(Parser):
	@rule("species","(",List(Rule("param"), ","),")", out="S")
	def _(_1, _2, l, _3):
		return Node("specie", *l)

	@rule("atoms","=","'",List(Rule("atom"), " "),"'", out="param")
	def _(k, _1, _2, v, _3):
		return Node(k, *v)
	@rule("thermo","=","(",List(Rule("nasa"),","),")", out="param")
	def _(k, _1, _2, v, _3):
		return Node(k, *v)
	@rule("transport","=","gas_transport","(",List(Rule("kv"),","),")", out="param")
	def _(k, _1, _2, _3, v, _4):
		return Node(k, *v)
	@rule(Rule("kv"), out="param")
	def _(_1):
		return _1

	@rule(WORD,"=",Rule("value"), out="kv")
	def _(k, _1, v):
		return Node(k, v)

	@rule(Rule("number"), out="value")
	def _(_1): return _1
	@rule('"',WORD,'"', out="value")
	def _(_1, v, _2): return v
	@rule("'",WORD,"'", out="value")
	def _(_1, v, _2): return v
	@rule("‘",WORD,"’", out="value")
	def _(_1, v, _2): return v

	@rule(WORD,":",Rule("number"), out="atom")
	def _(k, _1, v):
		return Node(k, v)

	@rule("NASA","(",List(Rule("numbers"),","),")", out="nasa")
	def _(k, _2, v, _3):
		return Node(k, *v)
	@rule("[",List(Rule("number"),","),"]", out="numbers")
	def _(_1, v, _2):
		return v

	@rule(SCNUM, out="number")
	def _(_1): return _1
	@rule(FLOAT, out="number")
	def _(_1): return _1
	@rule(NUM, out="number")
	def _(_1): return _1


if __name__ == "__main__":
	with open("chem.cti", "r") as f:
		t = f.read()
	p = myParser(t, verbose=False)
	while True:
		result = p.parse()
		if result is TokenNotFound:
			break
		print(result)
		print(result.to_dict())
		input(p.index)
