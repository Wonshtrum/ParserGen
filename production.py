def rule(*args, out="S"):
	class deco:
		def __init__(self, f):
			entry = (args, f)
			if out in rule.tmp:
				rule.tmp[out].append(entry)
			else:
				rule.tmp[out] = [entry]
		def __set_name__(self, owner, name):
			owner.rules = rule.tmp
			rule.tmp = {}
	return deco
rule.tmp = {}
