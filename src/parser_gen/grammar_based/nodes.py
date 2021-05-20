class Node:
	def __init__(self, type, *args, **kwargs):
		self.type = type
		self.args = list(args)
		for key, val in kwargs.items():
			if hasattr(val, "__iter__"):
				self.add(Node(key, *val))
			else:
				self.add(Node(key, val))
	def add(self, arg):
		self.args.append(arg)
		return self
	def __getitem__(self, key):
		values = [arg for arg in self.args if isinstance(arg, Node) and arg.type==key]
		if len(values) == 0:
			return None
		elif len(values) == 1:
			return values[0]
		return values
	def keys(self):
		return set(arg.type for arg in self.args if isinstance(arg, Node))
	def values(self):
		return [arg for arg in self.args if not isinstance(arg, Node)]
	def format(self, tab=''):
		dec = ' '
		result = self.type
		for i, arg in enumerate(self.args):
			result += '\n'+tab
			if i == len(self.args)-1:
				result += '└'
				pad = ' '
			else:
				result += '├'
				pad = '│'
			result += dec
			if isinstance(arg, Node):
				result += arg.format(tab+pad+dec)
			else:
				result += str(arg)
		return result
	def __repr__(self):
		return self.format()
