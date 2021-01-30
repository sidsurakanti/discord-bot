from .lexer import Lexer
from ._parser import Parser
from ._interpreter import Interpreter
from colorama import Fore, Style

def calc(expr):
	tokens = Lexer(expr).lexer()
	parsed = Parser(tokens).parse()
	results = Interpreter(parsed).run()
	return "".join(map(str, results))


if __name__ == "__main__":
	print('Type "quit" to quit the program')
	while True:
		print(Fore.GREEN + ">>>" + Style.RESET_ALL, end=" ")
		expression = input()
		if "quit" in expression:
			break
		print(calc(expression))
