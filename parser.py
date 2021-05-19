import re

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
		self.expr = re.compile(pattern, re.DOTALL)
	def match(self, *args, **kwargs):
		return self.expr.match(*args, **kwargs)
	def __repr__(self):
		return f"Regex('{self.pattern}')"

class List:
	def __init__(self, element, separator):
		self.element = element
		self.separator = separator
	def __repr__(self):
		return f"List('{self.element}', '{self.separator}')"
	def __iter__(self):
		return iter((self.element, self.separator))

DEBUG = False
DEFAULT_DELIM = [' ', '\n', '\t']
class Parser:
	def __init__(self, rules, text, delim=DEFAULT_DELIM):
		self.index = 0
		self.rules = rules
		self.delim = delim
		self.text = text
		self.length = len(text)
	
	def head(self):
		if self.index < self.length:
			return self.text[self.index]
		return None
	
	def view(self, n=1):
		return self.text[self.index-n:self.index+n]

	def _eat(self, token):
		if isinstance(token, Regex):
			match = token.match(self.text[self.index:])
			if match is None:
				return False
			self.index += match.end()
			return match.group()
		if not isinstance(token, str):
			raise TypeError
		length = len(token)
		if self.text[self.index:self.index+length] == token:
			self.index += length
			return token
		return False
	def eat(self, token):
		while True:
			result = self._eat(token)
			if result is not False or self.head() not in self.delim:
				return result
			self.index += 1

	def parse(self, goal=Rule("S"), degree=0):
		if isinstance(goal, List):
			element, separator = goal
			elements = []
			while True:
				result = self.parse(element, degree+1)
				if result is False:
					break
				elements.append(result)
				result = self.parse(separator, degree+1)
				if result is False:
					break
			if DEBUG:print(elements)
			return elements
		if not isinstance(goal, Rule):
			return self.eat(goal)
		index = self.index
		for rule in self.rules[goal.get()]:
			print(" "*degree, "TRYING", rule)
			self.index = index
			tree = []
			for token in rule:
				print(" "*degree, "- SEARCH", token)
				if DEBUG:input()
				result = self.parse(token, degree+1)
				if result is False:
					break
				tree.append(result)
			else:
				return tree
		return False


WORD  = Regex("\w+")
NUM   = Regex("[\+\-]?\d+")
FLOAT = Regex("[\+\-]?\d+\.\d+")
SCNUM = Regex("[\+\-]?\d+\.\d+[eE][\+\-]\d+")
