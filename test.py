from business_parser import parser
from lexer import LexerBusiness
from language import Evaluator, Scope, SemanticChecker

print("Insert file name ( '.bus' extension ) to run: ")
file_name = input()

with open('test/' + file_name + '.bus', 'r') as file:
    data = file.read()
l = LexerBusiness()
l.build()
node = parser.parse(data, lexer=l.lexer)
checker = SemanticChecker(Scope())
checker.visit(node)
evaluator = Evaluator(Scope()) 
evaluator.visit(node)
