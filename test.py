import re
from lexer import LexerBusiness

# p = re.compile(r'"[a-zA-Z_]*"')

# print(p.findall('"Jorge_Maricon" "Ernesto_Animal"'))

m = LexerBusiness()
m.build()
m.test('business b1 = {staff b1_staff = [employed e1 = {"Jorge", 300}]; catalog cat1 = [product p1 = {"Ropa", 13.5, 20}]}')