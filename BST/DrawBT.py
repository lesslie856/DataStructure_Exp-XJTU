import networkx as nx
import matplotlib.pyplot as plt
import math


def create_graph(G, node, pos={}, x=0, y=0, layer=4): # 类似先序遍历，对结点位置调整，
    pos[node.data] = (x, y)
    if node.lch:
        G.add_edge(node.data, node.lch.data)
        l_x, l_y = x - 1 / 1.5 ** layer, y - 1
        l_layer = layer + 1
        create_graph(G, node.lch, x=l_x, y=l_y, pos=pos, layer=l_layer)
    if node.rch:
        G.add_edge(node.data, node.rch.data)
        r_x, r_y = x + 1 / 1.5 ** layer, y - 1
        r_layer = layer + 1
        create_graph(G, node.rch, x=r_x, y=r_y, pos=pos, layer=r_layer)
    return G, pos


def draw(node, k, order, path):  # 以某个节点为根画图
    graph = nx.DiGraph()
    graph, pos = create_graph(graph, node)
    # fig=plt.figure()
    # fig,ax = plt.subplots(figsize=(10, 10))  # 比例可以根据树的深度适当调节
    fig = plt.figure(figsize=(25, 16))
    ax1 = fig.add_subplot(1, 1, 1)

    nx.draw_networkx(graph, pos, ax=ax1, node_size=1000, font_size=25, node_color='green')
    plt.title("The No.%d Tree figure" % k)
    plt.text(0.2, 0, order, fontsize=17)
    plt.text(0.2, -0.10, path, fontsize=17)
    plt.show()
