import ply.lex as lex
from datetime import date
class LexerBusiness:

    keywords = {
        "business" : "TYPE",
        "employed" : "TYPE",
        "product" : "TYPE",
        "collection" : "TYPE",
        "num" : "TYPE",
        "def" : "DEF",
        "return" : "RETURN",
        "bill" : "BILL",
        "void" : "VOID",
        "action" : "ACTION",
        "sale" : "SALE",
        "invest" : "INVESTS",
        "net_sales" : "METRICS",
        "gross_margin" : "METRICS",
        "gross_profit" : "METRICS",
        "expenses" : "METRICS",
        "earnings" : "METRICS",
        "print" : "PRINT",
        "load" : "LOAD",
        "save" : "SAVE",
        "amount" : "AMOUNT",
        "get" : "GET",
        "add" : "ADD",
        "del" : "DEL",
        "load" : "LOAD",
        "today" : "DATE",
        "last_week" : "DATE",
        "last_month" : "DATE",
        "last_year" : "DATE",
        "price" : "PRICE",
        "cost" : "COST",
        "if" : "IF",
        "else" : "ELSE",
        "foreach" : "FOREACH",
        "while" : "WHILE",
        "from" : "FROM",
        "in" : "IN",
        "not" : "NOT",
        "and" : "AND",
        "or" : "OR",
        "dismiss" : "DISMISS",
        "staff" : "STAFF",
        "while" : "WHILE",
        "catalog" : "CATALOG",
        "salary" : "SALARY",
        
    }

    tokens = [
        'POINT',
        'DPOINT',
        'OBR', #[
        'CBR', #]
        'OPAREN',
        'CPAREN',
        'OBRACE', #{
        'CBRACE', #}
        'ASSIGN', #=
        'EQUAL', #==
        'GEQ', #>=
        'LEQ', #<=
        'GREATER', #>
        'LESS', #<
        'PLUS',
        'MINUS',
        'DIV',
        'MULT',
        'COMMA',
        'NAME',
        'NUMBER',
        'DESCRIP',
        'ID',
        'END'
    ] + list(keywords.values())

    # TOKENS

    t_POINT = r'\.'
    t_OBRACE = r'\{'
    t_CBRACE = r'\}'
    t_ASSIGN = r'='
    t_OPAREN = r'\('
    t_CPAREN = r'\)'
    t_EQUAL = r'=='
    t_GEQ= r'>='
    t_LEQ = r'<='
    t_GREATER = r'>'
    t_LESS = r'<'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_DIV = r'/'
    t_MULT = r'\*'
    t_COMMA = r','
    t_DPOINT = r':'
    t_END = r';'
    t_OBR = r'\['
    t_CBR = r'\]'
    t_DESCRIP = r'"[a-zA-Z][a-zA-Z_\s]*"'
    

    def t_NUMBER (self,t):
        r'\d+(\.\d+)?'
        try:
            t.value = float(t.value)
        except ValueError:
            print("Float value too large %d", t.value)
            t.value = 0
        return t

    def t_NAME(self,t):
        r'"[a-zA-Z_]*"'
        t.value = t.value[1:-1]
        return t
    

    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.keywords.get(t.value.lower(),'ID')
        return t

    t_ignore = " \t"


    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
        

    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
    
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self,data):
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok:
                 break
             print(tok)