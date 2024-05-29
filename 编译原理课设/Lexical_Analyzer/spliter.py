import sys

from Lexical_Analyzer.rules import *
import re
#对于经过Spec_Symbol_1中的单字符token，确定其类型
def type_assign(token):
    if token=='(':
        return token_type["LPAREN"]
    if token==')':
        return token_type["RPAREN"]
    if token=='[':
        return token_type["LBRACKET"]
    if token==']':
        return token_type["RBRACKET"]
    if token=='{':
        return token_type["LBRACE"]
    if token=='}':
        return token_type["RBRACE"]
    if token=='+':
        return token_type["ADD"]
    if token=='-':
        return token_type['SUB']
    if token=='/':
        return token_type['DIV']
    if token==',':
        return token_type['COMMA']
    if token==';':
        return token_type['SEMI']
    if token=='*':
        return token_type['MUL']

def check(token):
    reversed_word=['if','else', 'int' , 'return' , 'void' , 'while']
    id_parttern=r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    num_parttern=r'\b[0-9]+\b'
    if token in reversed_word:
        return token_type[token.upper()]
    elif re.fullmatch(id_parttern,token):
        return token_type['ID']
    elif re.fullmatch(num_parttern,token):
        return token_type['NUM']
    else:
        return token_type['error']
#针对一行进行扫描,依据DFA构建
def scan(line):
    index=0
    state=state_type['START']
    token=""
    # res存储元素形如(token,token_type)
    res=[]
    while index<len(line):
        c=line[index]
        # START状态
        if state==state_type['START']:
            token=""
            if c in spcace_word:
                index+=1
                continue
            elif c in Spec_Symbol_1:
                res.append((c,type_assign(c)))
                index+=1
                continue
            elif c =='=':
                state=state_type['EQ']
            elif c=='!':
                state=state_type['UNEQ']
            elif c=='<':
                state = state_type['LES']
            elif c=='>':
                state=state_type['LRG']
            elif c=='/':
                state=state_type['DIV']
            else:
                state=state_type['TEMP']
            token+=c
            index+=1
        elif state==state_type['DIV']:
            if c=='*':
                state=state_type['COMMENT1']
                token+=c
                index+=1
            else:
                res.append((token,token_type['DIV']))
                state=state_type['START']
        elif state==state_type['TEMP']:
            if c in Spec_Symbol_1 or c in Spec_Symbol_2 or c in spcace_word:
                res.append((token,check(token)))
                state=state_type['START']
            else:
                token+=c
                index+=1
        elif state==state_type['EQ']:
            if c=='=':
                token+=c
                res.append((token,token_type['EQ']))
                index += 1
            else:
                res.append((token,token_type['ASSIGN']))
            state=state_type['START']
        elif state==state_type['UNEQ']:
            if c=='=':
                token+=c
                res.append((token,token_type['UNEQ']))
                index += 1
            else:
                res.append((token,token_type['ASSIGN']))
            state=state_type['START']
        elif state==state_type['LES']:
            if c=='=':
                token+=c
                res.append((token,token_type['LE']))
                index+=1
            else:
                res.append((token,token_type['LT']))
            state=state_type['START']
        elif state==state_type['LRG']:
            if c=='=':
                token+=c
                res.append((token,token_type['GE']))
                index+=1
            else:
                res.append((token,token_type['GT']))
            state=state_type['START']
        elif state==state_type['COMMENT1']:
            if c=='*':
                token+=c
                index+=1
                state=state_type['COMMENT2']
            else:
                token+=c
                index+=1
        elif state==state_type['COMMENT2']:
            if c=='/':
                token+=c
                index+=1
                res.append((token,token_type['COM']))
                state=state_type['START']
            else:
                token+=c
                index+=1
                state=state_type['COMMENT1']
    return res



def split(file_path:str):
    list_value=list(token_type.values())
    list_key=list(token_type.keys())
    file=open(file_path,'r',encoding='utf-8')
    lines=[]
    for line in file.readlines():
        lines.append(line)
    res=[]
    for i in range(len(lines)):
        line=lines[i]
        t=scan(line)
        res.append(t)
    return res
        # for token in t:
        #     index=list_value.index(token[1])
        #     key=list_key[index]
        #     print('\t'+str(i+1)+': '+key+': '+token[0])

