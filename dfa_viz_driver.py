import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict

#transition table
# mat = [[2, 2], 
# 	 [3, 3],
# 	 [4, 4],
# 	 [5, 4],
# 	 [5, 6], 
# 	 [5, 7], 
# 	 [8, 9],
# 	 [10, 11],
# 	 [12, 10], 
# 	 [5, 4], 
# 	 [5, 7], 
# 	 [5, 4]]

# mat2 = [[1, 2],
# 		[3, 4],
# 		[5, 6],
# 		[1, 2],
# 		[3, 4],
# 		[5, 6],
# 		[3, 5]]
# finals = [7, 10, 11]


def isBetween(a: tuple, b: tuple, c: tuple) -> bool:

	'''
	to check if point c lies between point a and point b
	'''
	
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

def generate_node_positions(i: int, j: int, lim: int = 0) -> dict:
	
	'''
	returns a dictionary with node(number) as the key and the position they will be at
	in the i x j grid specified in the parameter
	'''
	
	pos, val = {}, 1
	lim = lim if lim else i*j
	for a in range(i):
		# if val == lim: break
		for b in range(j):
			pos[val] = [a, b]
			val += 1

	return pos

def generate_edge_positions(node_positions: dict, edgelist: list) -> tuple:

	'''
	returns two lists/sets of edges, 1st being the list of edges that have to be drawn straight and second
	which have to be drawn slightly curved
	it does this by checking if theres a node overlapping in the edge we wish to draw 
	'''
	
	curved_edges, straight_edges = set(), set()
	reverse_edge=set()

	for edge in edgelist:
	
		from_node_pos = node_positions[edge[0]]
		try:
			to_node_pos = node_positions[edge[1]]
		except KeyError:
			print("----------errr-------------")
			print(edgelist,node_positions, edge[1])
		crosses_node = False

		for between_node in node_positions:
			between = node_positions[between_node]
			
			if isBetween(from_node_pos, to_node_pos, between):
				if edge[0] == between_node or edge[1] == between_node or edge[0] == edge[1]:
					if edge in reverse_edge:
						pass
					else: continue
				crosses_node = True
				break

		if crosses_node:
			curved_edges.add(edge)
		else:
			straight_edges.add(edge)
		reverse_edge.add((edge[1], edge[0]))
	
	# print("straight_edges ->",straight_edges)
	# print("curved_edges ->", curved_edges)
	
	return (straight_edges, curved_edges)

def get_edge_labels(mat: list)->dict:

	'''
	returns a dictionary with edges as the key and the desired lable as the values
	(1, 2) = "0"
	'''
	
	res = defaultdict(str)
	for i, connection in enumerate(mat):
		res[(i+1, connection[0])] = "0" if (i+1, connection[0]) not in res else "0, 1"
		res[(i+1, connection[1])] = "1" if (i+1, connection[1]) not in res else "0, 1"

	return res

def mat_builder_nx(mat: list , G = nx.MultiDiGraph()) -> nx.MultiGraph:
	'''
	returns a networkx graph from the given transition table
	'''
	edge_color_key = {"0":'blue', '1':'red', "0, 1": "yellow"}	
	for i in range(1, len(mat)+1):
		G.add_node(i, label=rf"$q_{i}$", shape = 'o')

	E = get_edge_labels(mat)

	for i, state in enumerate(mat):
		# i, state = str(i), str(state)
		
		G.add_edge(i+1, state[0], color=edge_color_key[E[(i+1, state[0])]], width=2.5)
		G.add_edge(i+1, state[1], color=edge_color_key[E[(i+1, state[1])]], width=2.5)
	
	return G


#test
def ret_plot(mat, plt_im:plt, finals=[]):
	plt = plt_im
	G = mat_builder_nx(mat)

	positions = generate_node_positions(len(mat)//2 + 1, len(mat)//3 + 1, len(mat))
	
	G.poses = positions
	straight_edges, curved_edges = generate_edge_positions(positions, G.edges())
	edge_labels = get_edge_labels(mat)
	
	# colour map for final and non final states

	colour_map = ['lightblue' if i not in finals else 'lightgreen' for i in range(1, len(mat)+1 )]
	
	#draw nodes at the grid posisions and label

	nx.draw_networkx_nodes(G, pos = positions, node_size=700, node_color = colour_map)
	

	# nx.draw_networkx_labels(G, pos=positions)
	nx.draw_networkx_labels(G, positions, labels={node:G .nodes[node]['label'] for node in G.nodes()}, font_size=12, font_color='black', font_family='sans-serif', font_weight='normal', alpha=None, horizontalalignment='center')

	#draw staight edges
	zero_edges = [i for i in straight_edges if edge_labels[i]=="0"]
	one_edges = [i for i in straight_edges if edge_labels[i]=="1"]
	mixed_edges = [i for i in straight_edges if edge_labels[i]=="0, 1"]


	nx.draw_networkx_edges(G, pos=positions, edgelist=zero_edges, connectionstyle="arc3, rad=0.0", alpha=0.5, arrowstyle="->, head_length=0.8", width=1.5, edge_color="blue")
	nx.draw_networkx_edges(G, pos=positions, edgelist=one_edges, connectionstyle="arc3, rad=0.0", alpha=0.5, arrowstyle="->, head_length=0.8", width=1.5, edge_color="red")
	nx.draw_networkx_edges(G, pos=positions, edgelist=mixed_edges, connectionstyle="arc3, rad=0.0", alpha=0.5, arrowstyle="->, head_length=0.8", width=1.5, edge_color="black")


	#draw curved edges

	zero_edges = [i for i in curved_edges if edge_labels[i]=="0"]
	one_edges = [i for i in curved_edges if edge_labels[i]=="1"]

	nx.draw_networkx_edges(G, pos=positions, edgelist=zero_edges, connectionstyle="arc3, rad=0.2", alpha=0.5, arrowstyle="->, head_length=0.8", width=1.5, edge_color="blue")
	nx.draw_networkx_edges(G, pos=positions, edgelist=one_edges, connectionstyle="arc3, rad=0.2", alpha=0.5, arrowstyle="->, head_length=0.8", width=1.5, edge_color="red")


	#draw edge labels
	# nx.draw_networkx_edge_labels(G, positions, edge_labels=get_edge_labels(mat), label_pos=0.6)
	red_patch = mpatches.Patch(color='blue', label='0-> transitions')
	blue_patch = mpatches.Patch(color='red', label='1-> transitions')
	plt.legend(handles=[red_patch, blue_patch])
		 
	return G
# fig = plt.figure()
# mat_error = [[1, 2], [3, 4], [5, 1], [2, 3], [4, 5]]
# D = ret_plot(mat_error, fig)
# plt.show()
