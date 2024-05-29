import copy
from treelib import Node, Tree

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
n=5
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

# 创建树对象
tree = Tree()

# 添加根节点和子节点
tree.create_node("OP", "1",data="-")  # 根节点
tree.create_node("OP", "2", parent="1",data="/")
tree.create_node("ID", "3", parent="1",data="v")
tree.create_node("ID", "4", parent="2",data="u")
tree.create_node("ID", "5", parent="2",data="a")

# 显示树结构
print_tree(tree['2'].parent)


