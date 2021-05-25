def once_or_map(obj, f):
	if isinstance(obj, list):
		return [f(_) for _ in obj]
	return f(obj)


class Node:
	def __init__(self, type, *args, **kwargs):
		self.type = type
		self.args = list(args)
		for key, val in kwargs.items():
			if hasattr(val, "__iter__") and not isinstance(val, str):
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
	def values(self, collapse=False):
		values = [arg for arg in self.args if not isinstance(arg, Node)]
		if not collapse or len(values)>1:
			return values
		if len(values) == 1:
			return values[0]
		return None

	def to_dict(self, collapse=True):
		base = {key:once_or_map(self[key], lambda _:_.to_dict(collapse)) for key in self.keys()}
		if collapse and not base:
			return self.values(collapse)
		values = self.values()
		if len(values) or not collapse:
			base['values'] = self.values(collapse)
		if not collapse:
			base['_type'] = self.type
		return base

	def _format(self, tab=''):
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
				result += arg._format(tab+pad+dec)
			else:
				result += str(arg)
		return result
	def __repr__(self):
		return self._format()
