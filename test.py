from business_parser import parser
from lexer import LexerBusiness
from language import SemanticChecker, Scope

l = LexerBusiness()
l.build()
try:
    s = '''
    employed e1 = { "Ramon" , 30 }; 
    product p1 = { "Champu" };
    employed e2 = { "Juan" , 20 };
    product p2 = { "Papa" };
    
    collection c1 = [e1 , e2];

    collection c2 = [p1, p2];


    business b1 = {"Tienda" , c1 , c1 };
    '''
except EOFError:
    print("Error")
node = parser.parse(s, lexer=l.lexer)
checker = SemanticChecker(Scope())
checker.visit(node)
# p = re.compile(r'[a-zA-Z][a-zA-Z_\s]+')


