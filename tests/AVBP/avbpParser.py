from parser_gen.grammar_based import *


BLOB = Regex("[^ |:]+")
LINE = Regex("_+")
UNDERLINE = Regex("-+")
class coreParser(Parser):
	@rule(LINE, List(Rule("section"), min=1), out="S")
	def _(_1, l):
		return Node("table", *l)
	@rule(Rule("title"), Rule("sep"), List(Rule("line"), min=1), Rule("sep"), out="section")
	def _(title, _1, l, _2):
		return Node(title, *l)

	@rule("|", LINE, "|", out="sep")
	def _(_1, v, _2):
		return True

	@rule("|", List(BLOB), "|", out="title")
	def _(_1, v, _2):
		return " ".join(v)
	@rule("|", LINE, "|", out="line")
	def _(_1, v, _2):
		return False
	@rule("|", List(BLOB), ":", List(BLOB), "|", out="line")
	def _(_1, k, _2, v, _3):
		k = " ".join(k)
		v = " ".join(v)
		return Node(k, v)
	@rule("|", List(BLOB), "|", out="line")
	def _(_1, l, _2):
		if not l or all(UNDERLINE.match_all(_) for _ in l):
			return None
		return l

	def skip(self):
		index = self.text[self.index:].index('\n')
		if index == -1:
			self.eof()
			return False
		self.index += index+1
		return True


if __name__ == "__main__":
	with open("Archive/avbp.o", "r") as f:
		t = f.read()
	p = coreParser(t, verbose=False)
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
