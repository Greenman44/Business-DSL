import ply.yacc as yacc
from lexer import tokens

def p_list_instructions(p):
    '''ListInst : ListInst Instruction
                | Instruction'''
    # TODO: logic of lisInst

def p_instruction(p):
    '''Instruction : dec_business_instruction
                   | dec_product_instruction
                   | dec_employed_instruction
                   | dec_catalog_instruction
                   | dec_staff_instruction
                   | if_instruction
                   | if_else_instruction
                   | for_instruction'''
    # TODO: logic of Instruction

def p_dec_business_instruction(p):
    'dec_business_instruction : Business ID : {buss}'
    # TODO: logic of dec_business_instruction

def p_buss(p):
    pass