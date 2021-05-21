from .entities import Rule, Regex, List
from .config import *
from .production import rule
import traceback


class Parser:
	def __init__(self, text, delim=DEFAULT_DELIM, verbose=VERBOSE, context=None):
		self.index = 0
		self.deepest = 0
		self.delim = delim
		self.text = text
		self.length = len(text)
		self.set_verbose(verbose)
		if context is None:
			self.context = self
		else:
			self.context = context

	def add_rules(self, other):
		for key, value in other.rules.items():
			if key in self.rules:
				self.rules[key].extend(value)
			else:
				self.rules[key] = value

	def set_verbose(self, verbose):
		if verbose:
			self.print = print
		else:
			self.print = lambda *args, **kwargs: None
	
	def head(self):
		if self.index < self.length:
			return self.text[self.index]
		return None
	def skip(self):
		raise NotImplementedError
	def eof(self):
		self.index = self.length
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
	def _autoReset(f):
		def wrapper(self, *args, **kwargs):
			index = self.index
			result = f(self, *args, **kwargs)
			if result is False:
				self.reset(index)
			return result
		return wrapper

	@_autoReset
	def parse(self, goal=Rule("S"), depth=0):
		if isinstance(goal, List):
			element, separator = goal
			elements = []
			count = 0
			while count != goal.max:
				result = self.parse(element, depth+1)
				if result is False:
					break
				if result is not None:
					elements.append(result)
					count += 1
				result = self.parse(separator, depth+1)
				if result is False:
					break
			return elements if count >= goal.min else False
		if not isinstance(goal, Rule):
			return self.eat(goal)
		index = self.index
		for rule, constructor, n in self.rules[goal.get()]:
			self.print(" "*depth, "TRYING", rule)
			self.reset(index)
			tree = []
			for token in rule:
				self.print(" "*depth, "- SEARCH", token)
				result = self.parse(token, depth+1)
				if result is False:
					self.print(" "*depth, "ABORT")
					break
				tree.append(result)
			else:
				try:
					if len(tree) == n:
						return constructor(*tree)
					return constructor(*tree, self.context)
				except Exception as error:
					if not SMALL_TB:
						raise error
					traceback.print_exc()
					exit(-1)

		return False
