import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

mat = [[2, 2], 
	 [3, 3],
	 [4, 4],
	 [5, 4],
	 [5, 6], 
	 [5, 7], 
	 [8, 9],
	 [10, 11],
	 [12, 10], 
	 [5, 4], 
	 [5, 7], 
	 [5, 4]]
# mat = [[1, 2], 
# 	   [3, 3],
# 	   [1, 3]] 

plt.figure(figsize=(6,6))


def isBetween(a, b, c):
	crossproduct = (c[1] - a[1]) * (b[0] - a[0]) - (c[0] - a[0]) * (b[1] - a[1])

	if abs(crossproduct) != 0:
		return False

	dotproduct = (c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1])*(b[1] - a[1])
	if dotproduct < 0:
		return False

	squaredlengthba = (b[0] - a[0])*(b[0] - a[0]) + (b[1] - a[1])*(b[1] - a[1])
	if dotproduct > squaredlengthba:
		return False

	return True

def generate_node_positions(i, j, lim=None):
	pos, val = {}, 1
	lim = lim if lim else i*j
	for a in range(i):
		if val == lim: break
		for b in range(j):
			pos[val] = [a, b]
			val += 1

	print("positions = ", pos)
	return pos

def generate_edge_positions(node_positions, edgelist):
	curved_edges, straight_edges = set(), set()
	reverse_edge=set()
	for edge in edgelist:
		from_node_pos = node_positions[edge[0]]
		to_node_pos = node_positions[edge[1]]
		crosses_node = False
		for between_node in node_positions:
			between = node_positions[between_node]
			if isBetween(from_node_pos, to_node_pos, between):
				if edge[0] == between_node or edge[1] == between_node or edge[0] == edge[1]:
					if edge in reverse_edge:
						pass
					else: continue
				crosses_node = True
				print(edge, between_node)
				# break
		print(crosses_node)
		if crosses_node:
			curved_edges.add(edge)
		else:
			straight_edges.add(edge)
		reverse_edge.add((edge[1], edge[0]))
	print("straight_edges ->",straight_edges)
	print("curved_edges ->", curved_edges)
	return (straight_edges, curved_edges)

def get_edge_labels(mat):
	res = {}
	for i, connection in enumerate(mat):
		# print(i, connection[0], "---", i, connection[1])
		res[(i+1, connection[0])] = "0" if (i+1, connection[0]) not in res else "0, 1"
		res[(i+1, connection[1])] = "1" if (i+1, connection[1]) not in res else "0, 1"

	return res

def mat_builder(mat: list , G = nx.MultiDiGraph()):
	for i in range(1, len(mat)+1):
		G.add_node(i)

	for i, state in enumerate(mat):
		# i, state = str(i), str(state)
		G.add_edge(i+1, state[0])
		G.add_edge(i+1, state[1])
	return G

G = mat_builder(mat)

positions = generate_node_positions(4, 4, 12)
straight_edges, curved_edges = generate_edge_positions(positions, G.edges())

print("curved_edges ->>", curved_edges)
pos = nx.spring_layout(G, k = 1.5)
nx.draw_networkx_nodes(G, pos=positions, node_size=700, node_color='lightblue')
nx.draw_networkx_labels(G, pos=positions)
nx.draw_networkx_edges(G, pos=positions, edgelist=straight_edges, connectionstyle="arc3, rad=0.0", alpha=0.3, arrowstyle="->, head_length=0.8")
nx.draw_networkx_edges(G, pos=positions, edgelist=curved_edges, connectionstyle="arc3, rad=0.15", alpha=0.3, arrowstyle="->, head_length=0.8")
nx.draw_networkx_edge_labels(G, positions, edge_labels=get_edge_labels(mat), label_pos=0.6)
# plt.axis('off')
plt.show()