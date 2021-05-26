from .entities import Regex


WORD   = Regex("\w+", "WORD")
NUM    = Regex("[\+\-]?\d+", "NUM")
FLOAT  = Regex("[\+\-]?\d+\.\d+", "FLOAT")
SCNUM  = Regex("[\+\-]?\d+\.?\d*[eE][\+\-]\d+", "SCNUM")
STRING = Regex(r"(?:\\.|[^\"])*", "STRING")
