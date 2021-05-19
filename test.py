from parser import *

D = {}
D["S"] = [
	("species","(",List(Rule("param"), ","),")")
	]
D["param"] = [
	("atoms","=","'",List(Rule("atom"), " "),"'"),
	("thermo","=","(",List(Rule("nasa"),","),")"),
	("transport","=","gas_transport","(",List(Rule("kv"),","),")"),
	(Rule("kv"),)
	]
D["kv"] = [
	(WORD,"=",Rule("value"))
	]
D["value"] = [
	(Rule("number"),),
	('"',WORD,'"'),
	("'",WORD,"'"),
	("‘",WORD,"’")
	]
D["atom"] = [
	(WORD,":",Rule("number"))
	]
D["nasa"] = [
	("NASA","(",List(Rule("numbers"),","),")")
	]
D["numbers"] = [
	("[",List(Rule("number"),","),"]")
	]
D["number"] = [
	(SCNUM,),
	(FLOAT,),
	(NUM,)
	]


with open("text", 'r') as f:
	t = f.read()
p = Parser(D,t)
