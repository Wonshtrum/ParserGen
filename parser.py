from entities import Rule, Regex, List
from config import *
from production import rule


if VERBOSE:
	print_debug = print
else:
	print_debug = lambda *args, **kwargs: None

class Parser:
	def __init__(self, text, delim=DEFAULT_DELIM):
		self.index = 0
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
			return elements
		if not isinstance(goal, Rule):
			return self.eat(goal)
		index = self.index
		for rule, constructor in self.rules[goal.get()]:
			print_debug(" "*degree, "TRYING", rule)
			self.index = index
			tree = []
			for token in rule:
				print_debug(" "*degree, "- SEARCH", token)
				result = self.parse(token, degree+1)
				if result is False:
					break
				tree.append(result)
			else:
				return constructor(*tree)
		return False
