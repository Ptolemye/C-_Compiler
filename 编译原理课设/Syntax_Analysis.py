from Lexical_Analyzer import spliter
from Lexical_Analyzer import rules
from treelib import Node, Tree
from LL1 import *
import pandas as pd
#做一下预处理
In_stream=spliter.split("test/test2.txt")
list_value=list(rules.token_type.values())
list_key=list(rules.token_type.keys())
#ch_stream:输入token流，流中每个元素型为(token,type)
ch_stream=[]
for i in In_stream:
    for j in i:
        index=list_value.index(j[1])
        key=list_key[index]
        if key!='COM':
            ch_stream.append((j[0],key))

def delete_node(tree, node_id):
    node = tree.get_node(node_id)
    parent_id = node.predecessor(tree.identifier)  # 使用 node.predecessor

    # 获取要删除节点的子节点
    parent_children = tree.children(parent_id)

    # 如果要删除节点有父节点，重新分配子节点到父节点
    if parent_id:
        for brother in parent_children:
            if brother.identifier==node_id:
                target_child=tree.children(node_id)
                for child in target_child:
                    tree.move_node(child.identifier,parent_id)
            else:
                tree.move_node(brother.identifier,parent_id)
        tree.remove_node(node_id)


def print_tree(tree, node_id, indent=""):
    """
    递归打印树结构
    """
    node = tree.get_node(node_id)
    if node.data !="":
        print(indent + node.tag + ":"+node.data)
    else:
        print(indent + node.tag)
    children = tree.children(node_id)
    for child in children:
        print_tree(tree, child.identifier, indent + "\t")

#模拟LL1分析逻辑
node_id=1
stack=['$',('program',node_id)]
Input=[]
for t in ch_stream:
    Input.append(t)
Input.append(('$','$'))

Analysis_tree=Tree()
Analysis_tree.create_node("program",str(node_id),data="")

while True:
    if stack==["$"] and Input==[('$','$')]:
        break
    #取出栈顶元组(,node_id)
    stack_top=stack[-1]
    stack_parser=stack_top[0]
    father_id=stack_top[1]
    Input_ch=Input[0]
    token = Input_ch[0]
    token_type = Input_ch[1]
    if stack_parser in non_terminal_set:
        #获取表达式
        production=LL1[(stack_parser,token_type)].copy()
        #production.reverse()
        #消除栈顶元素，逆序入栈
        stack.pop()
        template_stack=[]
        for t in production:
            node_id+=1
            if t == "E":
                Analysis_tree.create_node(t, str(node_id), parent=str(father_id),data="")
                continue
            else:
                Analysis_tree.create_node(t, str(node_id), parent=str(father_id),data="")
                template_stack.append((t,node_id))
        template_stack.reverse()
        stack.extend(template_stack)
    elif stack_parser in terminal_set:
        if stack_parser==token_type:
            Analysis_tree[str(father_id)].data=token
            stack.pop()
            Input.pop(0)

# 分析树化为语法树
to_delete=[]
def OP_up(tree, node_id):
    node = tree.get_node(node_id)
    if node:
        if node.tag in OP:
            parent_id = node.predecessor(tree.identifier)
            parent_node=tree.get_node(parent_id)
            g_parent_id=parent_node.predecessor(tree.identifier)
            g_parent_node = tree.get_node(g_parent_id)
            g_parent_node.tag='OP'
            g_parent_node.data=node.data
        for child in tree.children(node.identifier):
            OP_up(tree, child.identifier)
def Get_to_delete(tree, node_id):
    node = tree.get_node(node_id)
    if node:
        if node.tag not in reserved_process:
            to_delete.append(node.identifier)
        for child in tree.children(node.identifier):
            Get_to_delete(tree, child.identifier)
OP_up(Analysis_tree,Analysis_tree.root)
Get_to_delete(Analysis_tree,Analysis_tree.root)
for id in to_delete:
    delete_node(Analysis_tree,id)
print_tree(Analysis_tree,Analysis_tree.root)