from sys import stderr

def rule(*args, out="S"):
	class deco:
		def __init__(self, f):
			n = f.__code__.co_argcount
			if len(args)+1 < n or len(args) > n:
				print(f"  File \"{f.__code__.co_filename}\", line {f.__code__.co_firstlineno}\nConstructor '{out}': number of arguments doesn't match production rule", file=stderr)
				exit(-1)
			entry = (args, f, n)
			if out in rule.tmp:
				rule.tmp[out].append(entry)
			else:
				rule.tmp[out] = [entry]
		def __set_name__(self, owner, name):
			owner.rules = rule.tmp
			rule.tmp = {}
	return deco
rule.tmp = {}
