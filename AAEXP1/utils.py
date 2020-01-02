import networkx as nx
import random as rd
from math import floor,sqrt
import matplotlib.pyplot as plt

plot = 0
	
# Creates a random directed graph
def random_flow_graph(option = 0, n_nodes = 0, max_capacity = 10):
	if option:
		if not n_nodes and option > 9:
			n_nodes = rd.randint(2,30)
	elif n_nodes:
		option = 20
	else:
		option = rd.randint(1,50)
		n_nodes = rd.randint(2,30)		
	
	if option > 0 and option <= 5:
		G = nx.DiGraph()
		G.add_edge(0,1,capacity=10)
		G.add_edge(1,2,capacity=1)
		G.add_edge(1,5,capacity=1)
		G.add_edge(2,3,capacity=1)
		G.add_edge(3,4,capacity=1)
		G.add_edge(5,4,capacity=1)
		G.add_edge(4,8,capacity=1)
		G.add_edge(5,6,capacity=1)
		G.add_edge(6,7,capacity=1)
		G.add_edge(7,8,capacity=1)
		G.add_edge(8,9,capacity=10)
		s = 0
		t = 9
		t_prev = 8
	elif option > 5 and option <= 10:
		G = nx.DiGraph()
		G.add_edge(0,1,capacity=10)
		G.add_edge(1,2,capacity=1)
		G.add_edge(1,3,capacity=1)
		G.add_edge(2,4,capacity=1)
		G.add_edge(3,4,capacity=1)
		G.add_edge(4,5,capacity=1)
		G.add_edge(4,6,capacity=1)
		G.add_edge(3,6,capacity=1)
		G.add_edge(5,7,capacity=1)
		G.add_edge(6,7,capacity=1)
		G.add_edge(6,8,capacity=1)
		G.add_edge(7,8,capacity=1)
		G.add_edge(8,9,capacity=10)
		s = 0
		t = 9
		t_prev = 8
	else:
		G = nx.generators.gn_graph(n_nodes)
		# Add capacity attribute
		attrs = {(e1,e2):{'capacity':rd.randint(1,max_capacity)} for e1,e2 in G.edges()}
		nx.classes.function.set_edge_attributes(G,attrs)
		
		# Random number of nodes connected to source and sink
		num_starts = rd.randint(1,floor(sqrt(n_nodes)))
		num_ends = rd.randint(1,floor(sqrt(n_nodes)))
		
		# Get those nodes
		if num_ends == 1:
			ends = set([0])
		else:
			ends = set(rd.sample([n for n in G.nodes() if G.in_degree(n) >= 1],num_ends))
			
		starts = rd.sample([n for n in G.nodes() if G.out_degree(n) >= 1 and n not in ends],num_starts)
		
		# Create source and sink
		s = len(G.nodes()) + 1
		t = s + 1
		
		# Connect source to start nodes
		for sn in starts:
			G.add_edge(s,sn,capacity=max_capacity+1)
		
		# Connect end nodes to sink
		for en in ends:
			G.add_edge(en,t,capacity=max_capacity+1)
	
	# Solve max-flow
	R = nx.algorithms.flow.edmonds_karp(G,s,t)
	expected = sum([R[e1][e2]['flow'] for e1,e2 in R.edges() if e2 == t])
	
	return G, s, t, expected

# Show Graph
def draw(G,size=7):
    global plot
    plt.figure(plot,(size,size))
    pos = nx.circular_layout(G)
    labels = {(e1,e2):G.edges[e1,e2]['capacity'] for e1,e2 in G.edges()}
    nx.draw_networkx(G,pos)
    nx.draw_networkx_edges(G,pos,edgelist=G.edges(),with_labels=True)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels,edgelist=G.edges())
    plt.show()
    plot += 1
