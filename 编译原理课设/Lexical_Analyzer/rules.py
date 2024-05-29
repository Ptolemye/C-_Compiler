Spec_Symbol_1=['(',')','[',']','{','}',';',',','+','-','*']
Spec_Symbol_2=['=','>','<','!','/']
spcace_word=['\n','\t',' ']
token_type={
    "REVERSED":1,#保留字
    "ID":2,#标识符
    "NUM":3,#数字
    "ADD":4,#加 +
    "SUB":5,#减 -
    "MUL":6,#乘 *
    "DIV":7,#除 /
    "LT":8,# <
    "LE":9,# <=
    "GT":10,# >
    "GE":11,# >=
    "EQ":12,# ==
    "ASSIGN":13,# =
    "UNEQ":14,# !=
    "LPAREN":15,# (
    "RPAREN":16,# )
    "LBRACKET":17,# [
    "RBRACKET":18,# ]
    "LBRACE":19,# {
    "RBRACE":20,# }
    "COM":21,# /**/
    "COMMA":22,# ,
    "SEMI":23,# ;
    "IF":24,# if
    "ELSE":25,# else
    "INT":26,# INT
    "RETURN":27,#return
    "VOID":28,#void
    "WHILE":29,#while
    "error":100
}

state_type={
    "START":1,
    "TEMP":2,
    "EQ":3,
    "UNEQ":4,
    "LES":5,
    "LRG":6,
    "DIV":7,
    "COMMENT1":8,
    "COMMENT2":9
}