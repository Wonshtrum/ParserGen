from entities import Rule, Regex, List
from config import *
from production import rule
import traceback


if VERBOSE:
	print_debug = print
else:
	print_debug = lambda *args, **kwargs: None

class Parser:
	def __init__(self, text, delim=DEFAULT_DELIM):
		self.index = 0
		self.deepest = 0
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
	
	def reset(self, index=0):
		if self.index > self.deepest:
			self.deepest = self.index
		self.index = index

	def parse(self, goal=Rule("S"), depth=0):
		if isinstance(goal, List):
			element, separator = goal
			elements = []
			while True:
				result = self.parse(element, depth+1)
				if result is False:
					break
				if result is not None:
					elements.append(result)
				result = self.parse(separator, depth+1)
				if result is False:
					break
			return elements
		if not isinstance(goal, Rule):
			return self.eat(goal)
		index = self.index
		for rule, constructor, n in self.rules[goal.get()]:
			print_debug(" "*depth, "TRYING", rule)
			self.reset(index)
			tree = []
			for token in rule:
				print_debug(" "*depth, "- SEARCH", token)
				result = self.parse(token, depth+1)
				if result is False:
					break
				tree.append(result)
			else:
				try:
					if len(tree) == n:
						return constructor(*tree)
					return constructor(*tree, self)
				except Exception as error:
					if not SMALL_TB:
						raise error
					traceback.print_exc()
					exit(-1)

		return False
E=[]
