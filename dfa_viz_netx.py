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

def generate_positions(i, j):
	pos, val = {}, 1
	for a in range(i):
		for b in range(j):
			pos[val] = [a, b]
			val += 1
	print("positions = ", pos)
	return pos

positions = generate_positions(4, 4)

def mat_builder(mat: list , G = nx.MultiDiGraph()):
	for i in range(1, len(mat)+1):
		G.add_node(i)

	for i, state in enumerate(mat):
		# i, state = str(i), str(state)
		G.add_edge(i+1, state[0])
		G.add_edge(i+1, state[1])
	return G
def get_edge_labels(mat):
	res = {}
	for i, connection in enumerate(mat):
		# print(i, connection[0], "---", i, connection[1])
		res[(i+1, connection[0])] = "0" if (i+1, connection[0]) not in res else "0, 1"
		res[(i+1, connection[1])] = "1" if (i+1, connection[1]) not in res else "0, 1"
	print(res)
	return res

G = mat_builder(mat)
pos = nx.spring_layout(G, k = 1.5)
nx.draw(G, pos=positions, with_labels=True, node_size=700, width=0.4, node_color='lightblue')
nx.draw_networkx_edge_labels(G, positions, edge_labels=get_edge_labels(mat))
# plt.axis('off')
plt.show()