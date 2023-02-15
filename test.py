# from business_parser import parser
# from lexer import LexerBusiness
from business_data import  Collection, Product
# SemanticChecker, Scope,
# l = LexerBusiness()
# l.build()
# try:
#     s = '''
#     employed e1 = { "Ramon" , 30 }; 
#     product p1 = { "Champu" };
#     employed e2 = { "Juan" , 20 };
#     product p2 = { "Papa" };
    
#     collection c1 = [e1 , e2];

#     collection c2 = [p1, p2];

#     business b1 = {"Tienda" , c1 , c2 };

#     b1 ACTION SALE p1 price : 30.5 amount : 10.1;

# '''
# except EOFError:
#     print("Error")
# node = parser.parse(s, lexer=l.lexer)
# checker = SemanticChecker(Scope())
# checker.visit(node)
# p = re.compile(r'[a-zA-Z][a-zA-Z_\s]+')

c = Collection([Product("papa"), Product("tomate"), Product("cebolla")])

c.delete_coll(Collection([Product("papa"), Product("otro")]))

for item in c:
    print(item)