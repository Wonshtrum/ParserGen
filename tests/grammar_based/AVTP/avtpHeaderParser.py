from parser_gen.grammar_based import *


BLOB = Regex("[^ \n]+")
class headerParser(Parser):
	@rule(List(Rule("initParam"), min=1), out="S")
	def _(l):
		return Node("header", *l)

	@rule("*****", "Reads file", BLOB, List(Rule("kv"), min=1), out="initParam")
	def _(_1, _2, fname, l):
		return Node("file", *l, fname=fname)
	@rule("*****", "Info on initial grid :", List(Rule("kv")), out="initParam")
	def _(_1, _2, l):
		return Node("grid", *l)
	@rule("*****", "After partitioning :", List(Rule("kv")), out="initParam")
	def _(_1, _2, l):
		return Node("partition", *l)

	@rule(List(WORD, " ", min=1), ":", NUM, out="kv")
	def _(k, _1, v):
		k = ' '.join(k)
		return Node(k, v)
