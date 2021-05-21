from re import compile, DOTALL


def format_str(obj):
	if isinstance(obj, str):
		return repr(obj)
	return obj

class Rule:
	def __init__(self, name):
		self.name = name
	def __repr__(self):
		return f"Rule('{self.name}')"
	def get(self):
		return self.name

class Regex:
	def __init__(self, pattern, name=None):
		self.pattern = pattern
		self.expr = compile(pattern, DOTALL)
		self.name = name
	def match(self, *args, **kwargs):
		return self.expr.match(*args, **kwargs)
	def match_all(self, string):
		match = self.expr.match(string)
		if match is None:
			return False
		return match.end() == len(string)
	def __repr__(self):
		if self.name is None:
			return f"Regex({format_str(self.pattern)})"
		return f"{self.name}"

class List:
	def __init__(self, element, separator="", min=0, max=None):
		self.element = element
		self.separator = separator
		self.min = min
		self.max = max
	def __repr__(self):
		return f"List({format_str(self.element)}, {format_str(self.separator)})"
	def __iter__(self):
		return iter((self.element, self.separator))
