import ply.lex as lex

class LexerBusiness:

    keywords = {
        "business" : "BUSINESS",
        "employed" : "EMPLOYED",
        "product" : "PRODUCT",
        "staff" : "STAFF",
        "catalog" : "CATALOG",
        "if" : "IF",
        "else" : "ELSE",
        "for" : "FOR",
        "in" : "IN"
    }

    tokens = [
        'POINT',
        'DPOINT',
        'OBR',
        'CBR',
        'OBRACE',
        'CBRACE',
        'ASSIGN',
        'COMMA',
        'PCOMMA',
        'NAME',
        'NUMBER',
        'ID'
    ] + list(keywords.values())

    # TOKENS

    t_POINT = r'\.'
    t_OBRACE = r'\{'
    t_CBRACE = r'\}'
    t_DPOINT = r':'
    t_ASSIGN = r'='
    t_COMMA = r','
    t_PCOMMA = r';'
    t_OBR = r'\['
    t_CBR = r'\]'


    def t_NUMBER (self,t):
        r'\d+\.?\d+'
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