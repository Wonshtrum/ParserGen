import re


def add_var(variables):
	def wrapper(name, processor_name):
		processor = eval(processor_name) if processor_name is not None else None
		variables.append((name, processor, processor_name))
		return r"(\S.*?\S|\S)"
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

def repeat_char(x):
	return f"{re.escape(x)}{{2,}}"

def add_spaces(x):
	return f" {x.group()} "

def gen_regex(block):
	variables = []
	block = re.sub(r"{{.*?}}", add_spaces, block)
	block = [block.strip()]
	patterns = [
		(r"{{\s*}}", r".+?"),
		(r"{{\s*(\w+)(?:\s*:\s*(\w+))?\s*}}", add_var(variables)),
		(r"[+-]?\d+(?:\.\d+)?(?:[EeDd][+-]?\d+)?", r"\S+"),
		(r"\s+", r"\s*"),
		(r"([^a-zA-Z0-9])\1{2,}", repeat_char),
	]
	for a, b in patterns:
		block = multi_repl(a, a if b is None else b, block)
	block = "".join(text if i%2 else re.escape(text) for i, text in enumerate(block))
	return block, variables

class Parser:
	def __init__(self, template):
		blocks = [gen_regex(block) for block in template.split("(...)")]
		self.blocks = [(block, variables) for block, variables in blocks if variables]

	def parse(self, text, collapse=True, evaluate=True):
		output = {}
		for block, variables in self.blocks:
			n = re.compile(block).groups
			matches = re.findall(block, text)
			if n == 1:
				matches = [(_,) for _ in matches]
			matches = list(zip(*matches))
			for i, (name, processor, processor_name) in enumerate(variables):
				if matches:
					values = matches[i]
					if evaluate and processor is not None:
						try:
							output[name] = list(map(processor, values))
						except Exception:
							for value in values:
								try:
									processor(value)
								except Exception as error:
									print(f"Error: couldn't evaluate variable '{name}' with value '{value}' as '{processor_name}':")
									print(error)
									exit(-1)
					else:
						output[name] = list(values)
				else:
					output[name] = [None]
				if collapse and len(output[name]) == 1:
					output[name] ,= output[name]
		return output
