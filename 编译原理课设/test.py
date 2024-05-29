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

def delete_node(tree, node_id):
    # 检查节点是否存在
    if node_id not in tree.nodes:
        raise ValueError(f"Node {node_id} not found in the tree")

    node = tree.get_node(node_id)
    parent_id = node.predecessor(tree.identifier)  # 使用 node.predecessor

    # 获取要删除节点的子节点
    children = tree.children(node_id)

    # 如果要删除节点有父节点，重新分配子节点到父节点
    if parent_id:
        for child in children:
            tree.move_node(child.identifier, parent_id)
    else:
        # 如果没有父节点，这意味着我们试图删除根节点，这里需要特别处理
        if children:
            new_root = children[0]
            new_root_id = new_root.identifier
            for child in children[1:]:
                tree.move_node(child.identifier, new_root_id)
            tree.remove_node(node_id)
            # 重新设置新的根节点
            tree.root = new_root_id
            return tree

    # 删除目标节点
    tree.remove_node(node_id)

    return tree

# 创建树对象
tree = Tree()

# 添加根节点和子节点
tree.create_node("OP", "n"+str(1),data="")  # 根节点
tree.create_node("OP", "n2", parent="n1",data="/")
tree.create_node("ID", "n3", parent="n1",data="v")
tree.create_node("ID", "n4", parent="n2",data="u")
tree.create_node("ID", "n5", parent="n2",data="v")
tree=delete_node(tree,"n2")
tree["n5"].data="u"
# 显示树结构
print_tree(tree,tree.root)


