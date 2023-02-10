import ply.yacc as yacc
from lexer import tokens
from language import Program, TypeDeclaration, VariableAssignment, VariableCall, Metrics


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
                   | ID GET METRICS DATE'''
    if len(p) == 5:
        p[0] = Metrics(p[1], p[3], p[4])
    elif len(p) == 2:
        p[0] = p[1]

def p_instruction_sale(p):
    'Instruction : ACTION SALE ID PRICE DPOINT NUMBER amount DPOINT NUMBER'
    p[0] = ActionSALE(p[3], p[6], p[8])

def p_instruction_invests(p):
    'Instruction : ACTION INVESTS ID COST DPOINT NUMBER amount DPOINT NUMBER'
    p[0] = ActionINVESTS(p[3], p[6], p[8])

def p_instruction_add(p):
    '''Instruction : ID ADD ID
                   | ID ADD BILL OBRACE COST COMMA DESCRIP CBRACE'''
    p[0] = ActionADD(p[1], p[3])

def p_instruction_del(p):
    "Instruction : ID DEL ID"
    p[0] = ActionDEL(p[1], p[3])



def p_instance(p):
    '''instance : TYPE ID ASSIGN Assignable
                | ID ASSIGN Assignable'''
    if len(p) == 5:
        p[0] = TypeDeclaration(p[1], p[2], p[4])

    elif len(p) == 4:
        p[0] = VariableAssignment(p[1], p[3])

def p_Assignable(p):
    '''Assignable : OBRACE subType CBRACE
                  | OBR instance_list CBR
                  | ID'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

    #TODO: logic of buss

def p_subType(p):
    '''subType : bus
               | emp
               | prod'''
    p[0] = p[1]       
    #TODO: logic of dec_staff_instruction

def p_instance_list(p):
    '''instance_list : instance COMMA instance_list
                     | instance'''
    if len(p) ==  4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]

def p_instance_list_ID(p):
    '''instance_list : ID COMMA instance_list
                     | ID'''
    if len(p) ==  4:
        p[0] = [VariableCall(p[1])] + p[3]
    elif len(p) == 2:
        p[0] = [VariableCall(p[1])]

def p_bus(p):
    '''bus : instance COMMA instance'''
    p[0] = [p[1], p[3]]

def p_emp(p):
    '''emp : NAME COMMA NUMBER'''
    p[0] = [p[1], p[3]]

def p_prod(p):
    '''prod : NAME COMMA NUMBER COMMA NUMBER'''
    p[0] = [p[1], p[3], p[4]]

def p_error(p):
    raise Exception(f"Syntax error at '{p.value}', line {p.lineno} (Index {p.lexpos}).")

parser = yacc.yacc()