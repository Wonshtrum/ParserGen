from sys import stderr


class RuleDecorator:
	pass
def rule(*args, out="S"):
	class deco(RuleDecorator):
		def __init__(self, f):
			if isinstance(f, RuleDecorator):
				f = f.shared_f
			self.shared_f = f
			n = f.__code__.co_argcount
			if len(args)+1 < n or len(args) > n:
				print(f"  File \"{f.__code__.co_filename}\", line {f.__code__.co_firstlineno}\nConstructor '{out}': number of arguments doesn't match production rule", file=stderr)
				exit(-1)
			entry = (args, f, n)
			if out in rule.tmp:
				i = len(rule.tmp[out])
				while i > 0 and rule.tmp[out][i-1][1] is f:
					i -= 1
				rule.tmp[out].insert(i, entry)
			else:
				rule.tmp[out] = [entry]
		def __set_name__(self, owner, name):
			owner.rules = rule.tmp
			rule.tmp = {}
	return deco

rule.tmp = {}
