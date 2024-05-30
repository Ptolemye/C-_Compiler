import pandas as pd
import copy
# 读取Excel文件
file_path = '生成式 - 副本.xls'
df = pd.read_excel(file_path)
#非终结符集合
non_terminal_set = set(df['非终结符'].dropna())
#终结符集合
terminal_set=[
    "ID",#标识符
    "NUM",#数字
    "ADD",#加 +
    "SUB",#减 -
    "MUL",#乘 *
    "DIV",#除 /
    "LT",# <
    "LE",# <=
    "GT",# >
    "GE",# >=
    "EQ",# ==
    "ASSIGN",# =
    "UNEQ",# !=
    "LPAREN",# (
    "RPAREN",# )
    "LBRACKET",# [
    "RBRACKET",# ]
    "LBRACE",# {
    "RBRACE",# }
    "COM",# /**/
    "COMMA",# ,
    "SEMI",# ;
    "IF",# if
    "ELSE",# else
    "INT",# INT
    "RETURN",#return
    "VOID",#void
    "WHILE",#while
    "E"
]
punctuation=[
    "LPAREN",# (
    "RPAREN",# )
    "LBRACKET",# [
    "RBRACKET",# ]
    "LBRACE",# {
    "RBRACE",# }
    "COMMA",# ,
    "SEMI"# ;
]
tool1={
    "ID":"ID",
    "NUM":"NUM",
    "int":"INT",
    "void":"VOID",
    ",":"COMMA",
    ";":"SEMI",
    "if":"IF",
    "while":"WHILE",
    "return":"RETURN",
    "else":"ELSE",
    "(":"LPAREN",
    ")":"RPAREN",
    "[":"LBRACKET",
    "]":"RBRACKET",
    "{":"LBRACE",
    "}":"RBRACE",
    "+":"ADD",
    "-":"SUB",
    "*":"MUL",
    "/":"DIV",
    "!=":"UNEQ",
    "<":"LT",
    ">":"GT",
    ">=":"GE",
    "<=":"LE",
    "=":"ASSIGN",
    "==":"EQ",
    "E":"E"
}
reserved_process=[
    "program",
    "param",
    "var-declaration",
    "fun-declaration",
    "INT",
    "VOID",
    "params",
    "param",
    "compound-stmt",
    "selection-stmt",
    "ID",#标识符
    "NUM",#数字
    "COM",# /**/
    "INT",# INT
    "return-stmt",#return
    "VOID",#void
    "WHILE",#while
    "OP",
    "arg-list"
]
OP=[
    "ADD",#加 +
    "SUB",#减 -
    "MUL",#乘 *
    "DIV",#除 /
    "LT",# <
    "LE",# <=
    "GT",# >
    "GE",# >=
    "EQ",# ==
    "ASSIGN",# =
    "UNEQ",# !=
]
#产生式集合
def get_production_list(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 假设非终结符列名称为 '非终结符'，生成式列名称为 '生成式'
    non_terminal_column = '非终结符'
    production_column = '产生式'

    # 初始化空字典
    productions_dict = {}

    # 遍历每一行，读取非终结符和生成式
    for index, row in df.iterrows():
        non_terminal = row[non_terminal_column]
        production = row[production_column]

        # 根据空格分割生成式
        production_list = production.split()
        for i, token in enumerate(production_list):
            if token not in non_terminal_set:
                production_list[i]=tool1[token]
        # 如果非终结符不在字典中，初始化为一个空列表
        if non_terminal not in productions_dict:
            productions_dict[non_terminal] = []

        # 将分割后的生成式列表添加到相应的非终结符键下
        productions_dict[non_terminal].append(production_list)
    return productions_dict
production_list=get_production_list('生成式 - 副本.xls')

#获取产生式包含ε的非终结符
file_path = '生成式.xls'
sheet_name = 'Sheet1'
df = pd.read_excel(file_path, sheet_name=sheet_name)
non_terminal_toE = df[df['产生式'] == 'E']['非终结符'].tolist()
#求每个生成式的First集合
def Get_prodution_First(p_list):
    first=set()
    start=0
    while start<len(p_list):
        if p_list[start] in terminal_set:
            first.add(p_list[start])
            break
        if p_list[start] in non_terminal_set:
            first=first.union(Firstset[p_list[start]])
            first.discard("E")
            if p_list[start] in non_terminal_toE:
                if start==len(p_list)-1:
                    first.add("E")
                start+=1
            else:
                break
    return first
#生成每个非终结符的First集合
def Get_Firstset():
    Firstset={}
    #初始化Firt集
    for nt in production_list.keys():
        Firstset[nt]=set()
    Firstset_copy=copy.deepcopy(Firstset)
    while True:
        #若生成式第一个元素是终结符，则添加
        for nt,p_lists in production_list.items():
            for p_list in p_lists:
                if p_list[0] in terminal_set:
                    Firstset[nt].add(p_list[0])
        #合并产生式第一个元素是非终结符的First集
        for nt,p_lists in production_list.items():
            for p_list in p_lists:
                if p_list[0] in non_terminal_set:
                    Firstset[nt]=Firstset[nt].union(Firstset[p_list[0]])
                    Firstset[nt].discard("E")
        #考虑ε情况
        for nt, p_lists in production_list.items():
            for p_list in p_lists:
                for i in range(len(p_list)):
                    if p_list[i] in non_terminal_toE:
                        if i<len(p_list)-1:
                            Firstset[nt] = Firstset[nt].union(Firstset[p_list[i+1]])
                            Firstset[nt].discard("E")
                        elif i==len(p_list)-1:
                            Firstset[nt].add("E")
                            non_terminal_toE.append(nt)
                    else:
                        break
        if Firstset==Firstset_copy:
            break
        Firstset_copy=copy.deepcopy(Firstset)
    return Firstset

#生成每个非终结符的Follow集合
def Get_Followset():
    Followset={}
    #初始化Follow集合
    for nt in production_list.keys():
        Followset[nt]=set()
    Followset["program"].add("$")
    Followset_copy=copy.deepcopy(Followset)
    while True:
    #查看产生式后继
        for nt,p_lists in production_list.items():
            for p_list in p_lists:
                for i in range(len(p_list)-1):
                    if p_list[i] in non_terminal_set:
                        P=p_list[i+1:]
                        Followset[p_list[i]] = Followset[p_list[i]].union(Get_prodution_First(P))
                        # if p_list[i+1] in non_terminal_set:
                        #     Followset[p_list[i]]=Followset[p_list[i]].union(Firstset[p_list[i+1]])
                        #     Followset[p_list[i]].discard("E")
                        # elif p_list[i+1] in terminal_set:
                        #     Followset[p_list[i]].add(p_list[i+1])
    #结尾归并
        for nt,p_lists in production_list.items():
            for p_list in p_lists:
                end=len(p_list)-1
                while True:
                    if p_list[end] in terminal_set or end<0:
                        break
                    if p_list[end] in non_terminal_set:
                        Followset[p_list[end]]=Followset[p_list[end]].union(Followset[nt])
                    if p_list[end] in non_terminal_toE:
                        end-=1
                    else:
                        break
        if Followset==Followset_copy:
            break
        Followset_copy=copy.deepcopy(Followset)
    return Followset

#生成First集合和Follow集合
Firstset=Get_Firstset()
Followset=Get_Followset()


#生成M[N,T]
LL1={}
for nt,p_lists in production_list.items():
    for p_list in p_lists:
        first=Get_prodution_First(p_list)
        # first集添加
        for t in first:
            LL1[(nt,t)]=p_list
        # ε情况
        if "E" in first:
            for t in Followset[nt]:
                LL1[(nt, t)] = p_list
#就近原则挑选else
LL1[('selection-stmt#','ELSE')]=['ELSE' ,'statement']
# for non_terminal, first_set in Followset.items():
#     print(f"{non_terminal}: {first_set}")
