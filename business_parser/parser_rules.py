import ply.yacc as yacc
from lexer import tokens
from language import *


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
                   | ID GET METRICS DATE
                   | IF OPAREN condition CPAREN OBRACE ListInst CBRACE'''
    if len(p) == 5:
        p[0] = Metrics(VariableCall(p[1]), p[3], p[4])
    elif len(p) == 2:
        p[0] = p[1]
    
    elif len(p) == 8:
        p[0] = IfStatement(p[3], p[6])

def p_instruction_sale(p):
    'Instruction : ID ACTION SALE ID PRICE DPOINT NUMBER AMOUNT DPOINT NUMBER'
    p[0] = ActionSALE(VariableCall(p[1]), VariableCall(p[4]), p[7], p[10])

def p_instruction_invests(p):
    'Instruction : ID ACTION INVESTS ID COST DPOINT NUMBER AMOUNT DPOINT NUMBER'
    p[0] = ActionINVESTS(VariableCall(p[1]), VariableCall(p[4]), p[7], p[10])

def p_instruction_add(p):
    '''Instruction : ID ADD ID
                   | ID ADD BILL OBRACE COST CBRACE'''
    if len(p) == 4:
        p[0] = ActionADD(VariableCall(p[1]), VariableCall(p[3]))
    if len(p) == 7:
        p[0] = Bill_Node(VariableCall(p[1]), p[5])

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
                        | ID EQUAL ID
                        | ID LEQ ID
                        | ID GEQ ID
                        | ID GREATER ID
                        | ID LESS ID
                        '''

    if len(p) == 3:
        p[0] = NotStatement(p[2])
    elif len(p) == 4:
        p[0] = Bool_Expression_Node(p[1], p[3], p[2])

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

def p_instance_SAVELOAD(p):
    ''' instance : ID ASSIGN LOAD NAME
                 | SAVE ID '''
    if len(p) == 5:
        p[0] = Load(p[1],p[4])
    elif len(p) == 3:
        p[0] = Save(p[2])


def p_Assignable(p):
    '''Assignable : subType
                  | collection
                  '''
    p[0] = p[1]
    
    
def p_Assignable_ID(p):
    '''Assignable : ID'''
    p[0] = VariableCall(p[1])

def p_subType(p):
    '''subType : OBRACE bus CBRACE
               | OBRACE emp CBRACE
               | OBRACE prod CBRACE'''
    p[0] = p[2]       

def p_collection(p):
    "collection : OBR collection_body CBR"
    p[0] = Collection_Node(p[2])


def p_collection_body(p):
    '''collection_body : subType COMMA collection_body
                       | subType'''
    if len(p) ==  4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]

def p_collection_body_ID(p):
    '''collection_body : ID COMMA collection_body
                       | ID'''
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
    '''emp : NAME COMMA NUMBER'''
    p[0] = Emp_Node(p[1], p[3])

def p_prod(p):
    '''prod : NAME'''
    p[0] = Prod_Node(p[1])


def p_error(p):
    raise Exception(f"Syntax error at '{p.value}', line {p.lineno} (Index {p.lexpos}).")

parser = yacc.yacc()