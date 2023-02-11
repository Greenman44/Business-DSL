import ply.yacc as yacc
from lexer import tokens


def p_program(p):
    '''Program : ListInst'''


def p_list_instructions(p):
    '''ListInst : Instruction END ListInst
                | Instruction END'''
    # TODO: logic of listInst

def p_instruction(p):
    '''Instruction : instance'''
    # TODO: logic of Instruction

def p_instance(p):
    '''instance : dec_type
                | assign_inst'''

def p_dec_type(p):
    '''dec_type : Type ID ASSIGN Assignable'''
    
    # TODO: logic of type
        

def p_assign_inst(p):
    '''assign_inst : ID ASSIGN Assignable'''

    # TODO: logic of dec_business_instruction

def p_Assignable(p):
    '''Assignable : OBRACE subType CBRACE
                  | OBR instance_list CBR
                  | ID'''

    #TODO: logic of buss

def p_subType(p):
    '''subType : bus
               | emp
               | prod'''
                              
    #TODO: logic of dec_staff_instruction

def p_instance_list(p):
    '''instance_list : instance COMMA instance_list
                     | instance'''


def p_bus(p):
    '''bus : instance COMMA instance'''

def p_emp(p):
    '''emp : NAME COMMA NUMBER'''

def p_prod(p):
    '''prod : NAME COMMA NUMBER COMMA NUMBER'''
