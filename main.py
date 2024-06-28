import ply.yacc as yacc
import ply.lex as lex

reservados = {'INICIO': 'INICIO', 'MONITOR': 'MONITOR', 'EXECUTE': 'EXECUTE',
'TERMINO': 'TERMINO', 'ENQUANTO': 'ENQUANTO', 'FACA': 'FACA', 'FIM': 'FIM',
'IF': 'IF', 'THEN': 'THEN', 'ELSE': 'ELSE', 'EVAL': 'EVAL', 'ZERO': 'ZERO'
}

# Lista de tokens
tokens = ['PLUS', 'TIMES', 'EQUAL', 'COMMA', 
          'LPAREN', 'RPAREN', 'NUM', 'ID'] + list(reservados.values())

# Definições de tokens
t_EQUAL = r'='
t_COMMA = r','
t_PLUS = r'\+'
t_TIMES = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Definição de palavras reservadas, identificador e número
def t_reservados(t):
    r'[A-Z][A-Z]*'
    t.type = reservados.get(t.value, 'ID')
    return t
    
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t


def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Ignorar espaços e tabulações
t_ignore = ' \t\n'


# Tratamento de erros
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# Criação do lexer
lexer = lex.lex()
start = "programa"

var_monitorada = []

# Regras de gramática
def p_programa(p):
    'programa : INICIO varlist monitor_varlist EXECUTE cmds TERMINO'
    variaveis_prog = p[2].split(', ') + p[3].split(', ')
    inic_var = ""
    for variavel in variaveis_prog:
        inic_var += f"int {variavel} = 0;\n"
        if variavel in var_monitorada:
            inic_var += f'printf("{variavel} = %d",{variavel});'
    p[0] = f"#include <stdio.h>\n\nint main(){{\n{inic_var}\n{p[5]}\nreturn 0;\n}}"

def p_monitor_varlist(p):
    'monitor_varlist : MONITOR varlist'
    p[0] = p[2]
    tam = len(p[2].split(", "))
    global var_monitorada
    var_monitorada = var_monitorada[-tam:]


def p_varlist(p):
    """varlist : ID COMMA varlist
                | ID"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f'{p[1]}, {p[3]}'
    global var_monitorada
    var_monitorada.append(p[1])


def p_cmds(p):
    """cmds : cmd cmds
            | cmd"""
    if len(p) == 2:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}\n{p[2]}'


def p_cmd(p):
    """cmd : while
            | if
            | ifelse
            | plus
            | times
            | eval
            | zero
            | equal"""
    p[0] = p[1]


def p_while(p):
    'while : ENQUANTO ID FACA cmds FIM'
    p[0] = f"while ({p[2]})\n{{\n{p[4]}\n}}\n"


def p_if(p):
    'if : IF ID THEN cmd'
    p[0] = f"if ({p[2]})\n{{\n{p[4]}\n}}\n"


def p_if_else(p):
    'ifelse : IF ID THEN cmd ELSE cmd'
    p[0] = f"if ({p[2]})\n{{\n{p[4]}\n}}\nelse\n{{\n{p[6]}\n}}\n"


def p_eval(p):
    'eval : EVAL LPAREN ID COMMA ID COMMA cmds RPAREN'
    p[0] = f'for (int i = {p[3]}; i > {p[5]}; i--)\n{{\n{p[7]}}}\n'


def p_plus(p):
    """plus : ID PLUS exp
            | NUM PLUS exp"""
    p[0] = f"{p[1]} + {p[3]}"



def p_times(p):
    """times : ID TIMES exp
            | NUM TIMES exp"""
    p[0] = f'{p[1]} * {p[3]}'


def p_exp(p):
    """exp : ID
            | NUM
            | plus
            | times"""
    p[0] = p[1]


def p_zero(p):
    'zero : ZERO LPAREN ID RPAREN'
    p[0] = f'{p[3]} = 0;\n'
    if p[3] in var_monitorada:
        p[0] += f'printf("{p[3]} = %d",{p[3]});'


def p_equal(p):
    'equal : ID EQUAL exp'
    p[0] = f"{p[1]} = {p[3]};\n"
    if p[1] in var_monitorada:
        p[0] += f'printf("{p[1]} = %d",{p[1]});'


def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")


# Criação do parser
parser = yacc.yacc()

with open('ex2.provol', 'r') as file, open('saida.c', 'w') as file_saida:
    data = file.read()
    lexer.input(data)
    codigo_c = parser.parse(data)
    if codigo_c:
        file_saida.write(codigo_c)
        print("Arquivo .c gerado com sucesso!")
    else:
        print("Ocorreu um erro ao gerar o arquivo .c")

