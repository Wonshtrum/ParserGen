from parser_gen.grammar_based import *


__all__ = ["numberParser"]


class numberParser(Parser):
	@rule(SCNUM, out="number")
	def _(_1): return eval(_1)
	@rule(FLOAT, out="number")
	def _(_1): return float(_1)
	@rule(NUM, out="number")
	def _(_1): return int(_1)
