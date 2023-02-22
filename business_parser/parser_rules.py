import ply.yacc as yacc
from lexer import tokens
from language import *

#etecsa's fault

precedence = (
    ('left','PLUS','MINUS'),
    ('left','MULT','DIV'),
    )

def p_program(p):
    '''Program : ListInst'''
    p[0] = Program(p[1])


def p_list_instructions(p):
    '''ListInst : Instruction END ListInst
                | Instruction END'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    
    elif len(p) == 3:
        p[0] = [p[1]]

def p_instruction(p):
    '''Instruction : instance
                   | SAVE ID
                   | ID GET METRICS DATE
                   | loop_statements
                   | IfStatement
                   | IfStatement ELSE OBRACE ListInst CBRACE
                   '''
    if len(p) == 5:
        p[0] = Metrics(VariableCall(p[1]), p[3], p[4])
    elif len(p) == 2:
        p[0] = p[1]
    elif len(p) == 6:
        p[0] = ElseStatement(p[1], p[4])
    elif len(p) == 3:
        p[0] = Save(VariableCall(p[2]))


def p_instruction_sale(p):
    'Instruction : ID ACTION SALE ID PRICE DPOINT NUMBER AMOUNT DPOINT NUMBER'
    p[0] = ActionSALE(VariableCall(p[1]), VariableCall(p[4]), Number_Node(p[7]), Number_Node(p[10]))

def p_instruction_sale_ID(p):
    'Instruction : ID ACTION SALE ID PRICE DPOINT ID AMOUNT DPOINT ID'
    p[0] = ActionSALE(VariableCall(p[1]), VariableCall(p[4]), VariableCall(p[7]), VariableCall(p[10]))

def p_instruction_sale_operation(p):
    'Instruction : ID ACTION SALE ID PRICE DPOINT operation AMOUNT DPOINT operation'
    p[0] = ActionSALE(VariableCall(p[1]), VariableCall(p[4]), p[7], p[10])

def p_instruction_invests(p):
    'Instruction : ID ACTION INVESTS ID COST DPOINT NUMBER AMOUNT DPOINT NUMBER'
    p[0] = ActionINVESTS(VariableCall(p[1]), VariableCall(p[4]), Number_Node(p[7]), Number_Node(p[10]))

def p_instruction_invests_ID(p):
    'Instruction : ID ACTION INVESTS ID COST DPOINT ID AMOUNT DPOINT ID'
    p[0] = ActionINVESTS(VariableCall(p[1]), VariableCall(p[4]), VariableCall(p[7]), VariableCall(p[10]))

def p_instruction_invests_operation(p):
    'Instruction : ID ACTION INVESTS ID COST DPOINT operation AMOUNT DPOINT operation'
    p[0] = ActionINVESTS(VariableCall(p[1]), VariableCall(p[4]), p[7], p[10])

def p_instruction_add(p):
    '''Instruction : ID ADD ID
                   | ID ADD BILL OBRACE NUMBER COMMA DESCRIP CBRACE'''
    if len(p) == 4:
        p[0] = ActionADD(VariableCall(p[1]), VariableCall(p[3]))
    if len(p) == 9:
        p[0] = Bill_Node(VariableCall(p[1]), Number_Node(p[5]), p[7])

def p_instruction_Bill_oper(p):
    'Instruction : ID ADD BILL OBRACE operation COMMA DESCRIP CBRACE'
    p[0] = Bill_Node(VariableCall(p[1]), p[5], p[7])

def p_instruction_Bill_ID(p):
    'Instruction : ID ADD BILL OBRACE ID COMMA DESCRIP CBRACE'
    p[0] = Bill_Node(VariableCall(p[1]), VariableCall(p[5]),p[7])

def p_instruction_add_ID(p):
    ''' Instruction : ID ADD subType'''

    p[0] = ActionADD(VariableCall(p[1]),p[3])

def p_instruction_del(p):
    "Instruction : ID DEL NAME"
    p[0] = ActionDEL(VariableCall(p[1]), p[3])

def p_instruction_del_ID(p):
    "Instruction : ID DEL ID"
    p[0] = ActionDEL(VariableCall(p[1]), VariableCall(p[3]))

def p_instruction_dismiss(p):
    "Instruction : ID DISMISS NAME"
    p[0] = ActionDISMISS(VariableCall(p[1]), p[3])

def p_instruction_dismiss_ID(p):
    "Instruction : ID DISMISS ID"
    p[0] = ActionDISMISS(VariableCall(p[1]), VariableCall(p[3]))

def p_print(p):
    'Instruction : PRINT DPOINT ID'
    p[0] = Print_Node(VariableCall(p[3]))

def p_instruction_FuncCall(p):
    '''Instruction : funct_call'''
    p[0] = p[1]

def p_instruction_Func(p):
    '''Instruction : DEF TYPE NAME OPAREN Params CPAREN OBRACE ListInst CBRACE
                   | DEF VOID NAME OPAREN Params CPAREN OBRACE ListInst CBRACE'''
    p[0] = Function_Node(p[2], p[3], p[5], p[8])

def p_params(p):
    ''' Params : TYPE ID COMMA Params
               | TYPE ID
               | empty'''
    if len(p) == 5 or len(p) == 3:
        p[0] = Params_Node(p[1], p[2])

def p_loops_statements(p):
    '''loop_statements : FOREACH ID IN ID OBRACE ListInst CBRACE
                       | WHILE OPAREN condition CPAREN OBRACE ListInst CBRACE'''
    if p[1] == "foreach":
        p[0] = Foreach_node(p[2], VariableCall(p[4]), p[6])
    else:
        p[0] = While_node(p[3], p[6])

def p_IfStatement(p):
    "IfStatement : IF OPAREN condition CPAREN OBRACE ListInst CBRACE"
    p[0] = IfStatement(p[3], p[6])

def p_condition(p):
    '''condition : bool_expression
                '''
    
    if len(p) == 2:
        p[0] = p[1]



def p_bool_expression(p):
    '''
        bool_expression : NOT bool_expression
                        | bool_expression AND bool_expression
                        | bool_expression OR bool_expression
                        '''

    if len(p) == 3:
        p[0] = NotStatement(p[2])
    elif len(p) == 4:
        p[0] = Bool_Expression_Node(p[1], p[3], p[2])

def p_bool_expression_ID(p):
    '''bool_expression  : ID EQUAL ID
                        | ID LEQ ID
                        | ID GEQ ID
                        | ID GREATER ID
                        | ID LESS ID '''
    
    p[0] = Bool_Expression_Node(VariableCall(p[1]), VariableCall(p[3]), p[2])

def p_bool_expression_Paren(p):
    'bool_expression : OPAREN bool_expression CPAREN'

    p[0] = p[2]



def p_bool_expression_in(p):
    '''bool_expression : ID IN ID'''
    p[0] = InStatement(VariableCall(p[1]),VariableCall(p[3]))

def p_instance(p):
    '''instance : TYPE ID
                | TYPE ID ASSIGN Assignable
                | ID ASSIGN Assignable
                '''
                
    if len(p) == 3:
        p[0] = VariableDeclaration(p[1], p[2])

    elif len(p) == 5:
        p[0] = TypeDeclaration(p[1], p[2], p[4])

    elif len(p) == 4:
        p[0] = VariableAssignment(p[1], p[3])

def p_oper(p):
    ''' operation : operation PLUS operation
                  | operation MINUS operation
                  | operation DIV operation
                  | operation MULT operation
                  | ID'''
    if len(p) == 4:
        p[0] = Oper_Node(p[1],p[3],p[2])
    elif len(p) == 2:
        p[0] = VariableCall(p[1])

def p_oper_Number(p):
    'operation : NUMBER'
    p[0] =  Number_Node(p[1])

def p_oper_PAREN(p):
    ''' operation : OPAREN operation CPAREN'''
    p[0] = p[2]


def p_Assignable(p):
    '''Assignable : subType
                  | collection
                  | GET NAME FROM ID
                  | LOAD NAME
                  | operation
                  | funct_call
                  '''
    p[0] = p[1]
    if len(p) == 5:
        p[0] = GetElementFrom_Statement(p[2], VariableCall(p[4]))
    elif len(p) == 3:
        p[0] = Load(p[2])                  
                  

def p_Funct_call(p):
    '''Assignable : NAME OPAREN Assignable CPAREN'''
    p[0] = Funct_Call_Node(p[3])
        
def p_Assignable_Staff(p):
    '''Assignable : GET STAFF FROM ID'''
    p[0] = GetStaff_node(VariableCall(p[4]))
    
def p_Assignable_Catalog(p):
    '''Assignable : GET CATALOG FROM ID'''
    p[0] = GetCatalog_node(VariableCall(p[4]))

def p_Assignable_Amount(p):
    'Assignable : GET AMOUNT FROM ID'
    p[0] = GetAmount_node(VariableCall(p[4]))

def p_Assignable_ID(p):
    '''Assignable : ID'''
    p[0] = VariableCall(p[1])

def p_subType(p):
    '''subType : OBRACE bus CBRACE
               | OBRACE emp CBRACE
               | OBRACE prod CBRACE
               '''
    p[0] = p[2]       

def p_collection(p):
    '''collection : OBR collection_body CBR
                ''' 
    p[0] = Collection_Node(p[2])


def p_collection_body(p):
    '''collection_body : subType COMMA collection_body
                       | subType
                       '''
    if len(p) ==  4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]

def p_collection_body_empty(p):
    'collection_body : empty'
    p[0] = []

def p_collection_body_ID(p):
    '''collection_body : ID COMMA collection_body
                       | ID
                       '''
    if len(p) ==  4:
        p[0] = [VariableCall(p[1])] + p[3]
    elif len(p) == 2:
        p[0] = [VariableCall(p[1])]

def p_bus(p):
    '''bus : NAME COMMA collection COMMA collection'''           
    p[0] = Bus_Node(p[1], p[3], p[5])

def p_bus_ID(p):
    "bus : NAME COMMA ID COMMA ID"
    p[0] = Bus_Node(p[1], VariableCall(p[3]), VariableCall(p[5]))

def p_emp(p):
    '''emp : NAME COMMA SALARY DPOINT NUMBER'''
    p[0] = Emp_Node(p[1], Number_Node(p[5]))

def p_emp_ID(p):
    "emp : NAME COMMA SALARY DPOINT ID"
    p[0] = Emp_Node(p[1], VariableCall(p[5]))

def p_emp_Oper(p):
    'emp : NAME COMMA SALARY DPOINT operation'
    p[0] = Emp_Node(p[1], p[5])

def p_prod(p):
    '''prod : NAME COMMA AMOUNT DPOINT NUMBER
            | NAME'''
    if len(p) == 2:
        p[0] = Prod_Node(p[1])
    else:
        p[0] = Prod_Node(p[1], amount=Number_Node(p[5]))

def p_prod_ID(p):
    ' prod : NAME COMMA AMOUNT DPOINT ID'
    p[0] = Prod_Node(p[1], amount= VariableCall(p[5]))

def p_prod_Oper(p):
    'prod : NAME COMMA AMOUNT DPOINT operation'
    p[0] = Prod_Node(p[1], amount=p[5])

def p_empty(p):
    'empty :'
    pass


def p_error(p):
    raise Exception(f"Syntax error at '{p.value}', line {p.lineno} (Index {p.lexpos}).")

parser = yacc.yacc()