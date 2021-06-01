import re


def add_var(variables):
	def wrapper(name, processor):
		processor = eval(processor) if processor is not None else None
		variables.append((name, processor))
		return r"([^\s].*[^\s])"
	return wrapper

def _multi_repl(bulk, n, repl):
	if not callable(repl):
		res = repl
		repl = lambda *args: res
	return [bulk[0]]+[_
	for *sep, text in zip(*[iter(bulk[1:])]*(n+1))
	for _ in (repl(*sep), text)]

def multi_repl(pattern, repl, bulk):
	n = re.compile(pattern).groups
	return [_
	for i, element in enumerate(bulk)
	for _ in ([element] if i%2 else
	_multi_repl(re.split(pattern, element), n, repl))]

def gen_regex(block):
	variables = []
	block = [block.strip()]
	patterns = [
		(r"{{}}", r".+?"),
		(r"{{\s*(\w+)(?:\s*:\s*(\w+))?\s*}}", add_var(variables)),
		(r"[+-]?\d+(?:\.\d+)?(?:[EeDd][+-]?\d+)?", r"[^\s]+"),
		(r"\s+", None),
	]
	for a, b in patterns:
		block = multi_repl(a, a if b is None else b, block)
	block = "".join(text if i%2 else re.escape(text) for i, text in enumerate(block))
	return block, variables

class Parser:
	def __init__(self, template):
		blocks = self._blocks = [gen_regex(block) for block in template.split("(...)")]
		self.blocks = [(block, variables) for block, variables in blocks if variables]

	def parse(self, text, collapse=True, evaluate=True):
		output = {}
		for block, variables in self.blocks:
			n = re.compile(block).groups
			matches = re.findall(block, text)
			if n == 1:
				matches = [(_,) for _ in matches]
			print(matches)
			for ((name, processor), values) in zip(variables, zip(*matches)):
				if values:
					if evaluate and processor is not None:
						output[name] = list(map(processor, values))
					else:
						output[name] = list(values)
				else:
					output[name] = [None]
				if collapse and len(output[name]) == 1:
					output[name] ,= output[name]
		return output
