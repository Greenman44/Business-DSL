from business_parser import parser
from datetime import date, timedelta
from lexer import LexerBusiness
from language import Evaluator, Scope, SemanticChecker
# from business_data.data import  Collection, Product, Business_Data, Business, Employed, Number, Invest
import re
# from business_data import Number


# a =Collection([Employed( "prueba" , Number(300)), Employed("prueba2", Number(200))])
# print(a)
# print(a.__class__.__name__)
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


# print(int("09"))
# c1 = Collection([Product("papa"), Product("tomate"), Product("cebolla")])
# c2 = Collection([Employed("Juan", 30), Employed("Pepe", 20), Employed("Anacleto", 50)])
# c3 = Collection([Employed("Juan", 30),Employed("Antonio", 20)])

# a = Business("agro", c2, c1)

# a.data.make_invest(Invest(product=Product("tomate"), cost=50.0, amount=4))
# print(a.data.invests_table)
# a.data.Save_DatatoExcel()
# a = Business_Data.LoadBusiness("agro")
# print(a.data.invests_table)

# EXAMPLES
# ACTIONS



l = LexerBusiness()
l.build()

try:
    s =  '''



    def void Fibono(num c){
        num i = 1;
        num a = 0;
        num b = 1;
        while (i < c){
            num n = a + b;
            a = b;
            b = n;
            print: b;
            i = i + 1;
        };
        return;
    };
    num c = 8;
    Fibono(c);
    '''
except EOFError:
     print("Error")
node = parser.parse(s, lexer=l.lexer)
checker = SemanticChecker(Scope())
checker.visit(node)
evaluator = Evaluator(Scope()) 
evaluator.visit(node)
