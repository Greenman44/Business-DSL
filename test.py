from business_parser import parser
from lexer import LexerBusiness
from language import Evaluator, Scope, SemanticChecker
#from business_data.data import  Collection, Product, Business_Data, Business, Employed, Invest
# import re
# from business_data import Number

# a = Number(2)

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
# p = re.compile('\d+(\.\d+)?')
# print(p.fullmatch("3.56"))

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
#
try:
    s = '''
    employed e1 = {"Juan", salary : 300};
    employed e2 = {"Pedro", salary : 400};
    product p1 = {"Tomate", amount : 100};
    product p2 = {"Hierro", amount : 30};
    collection employeds = [e1, e2];
    collection products = [p1, p2];
    business b1 = {"DeTodo", employeds, products};
    num n1 = 20;
    num n2 = 5;
    num n3 = 10;
    num n4 = 30;

    b1 action sale p1 price: 20 amount: 5;
    b1 action sale p2 price: n1 amount: n2;
    b1 action invest p1 cost: 10 amount: 30;
    b1 action invest p1 cost: n3 amount: n4;
    b1 add {"Chirimolla", amount : 30};
    product p3 = {"Mamey", amount : 100};
    employed e3 = {"Alberto", salary : 500};
    b1 add p3;
    b1 add e3;
    b1 add bill {500, "Cobro de la luz"};
    b1 dismiss "Juan";
    save b1;
'''
    # b1 del p2;
    # b1 del "Tomate";
    # b1 dismiss e2;
    # b1 add e2;
    # b1 add p2;
    # b1 add e1;
    # b1 add p1;
except EOFError:
    print("Error")
node = parser.parse(s, lexer=l.lexer)
checker = SemanticChecker(Scope())
checker.visit(node)
evaluator = Evaluator(Scope()) 
evaluator.visit(node)

# OPERATIONS
# num n5 = (n4 + n3) * n2