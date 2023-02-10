# from business_parser import parser
# from lexer import LexerBusiness
import re 
# l = LexerBusiness()
# l.build()
# try:
#     s = 'employed e1 = { "Ramon" , 30 }; product p1 = { "Champu" , 15 , 30 };'
# except EOFError:
#     print("Error")
# r = parser.parse(s, lexer=l.lexer)
# print(r)
p = re.compile(r'[a-zA-Z][a-zA-Z_\s]+')

print(p.fullmatch('Jorge Maricon y ernesto es pato'))


