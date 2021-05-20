from re import compile, DOTALL

class Rule:
	def __init__(self, name):
		self.name = name
	def __repr__(self):
		return f"Rule('{self.name}')"
	def get(self):
		return self.name

class Regex:
	def __init__(self, pattern):
		self.pattern = pattern
		self.expr = compile(pattern, DOTALL)
	def match(self, *args, **kwargs):
		return self.expr.match(*args, **kwargs)
	def __repr__(self):
		return f"Regex('{self.pattern}')"

class List:
	def __init__(self, element, separator="", min=0, max=None):
		self.element = element
		self.separator = separator
		self.min = min
		self.max = max
	def __repr__(self):
		return f"List('{self.element}', '{self.separator}')"
	def __iter__(self):
		return iter((self.element, self.separator))
