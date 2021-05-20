from .entities import Regex

WORD  = Regex("\w+")
NUM   = Regex("[\+\-]?\d+")
FLOAT = Regex("[\+\-]?\d+\.\d+")
SCNUM = Regex("[\+\-]?\d+\.\d+[eE][\+\-]\d+")
