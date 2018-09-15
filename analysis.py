import pickle
import networkx as nx
import matplotlib.pyplot as plt
from nxviz import MatrixPlot, CircosPlot
from nxviz.plots import ArcPlot
from itertools import combinations
from collections import defaultdict

graph = pickle.load(open('github_users.p', 'rb'))

print("no. of users: "+str(len(graph.nodes())))
print("no. of user-collaborations(p2p) : "+str(len(graph.edges())))


plt.hist(list(nx.degree_centrality(graph).values()))
plt.show()



# Calculate the largest connected component subgraph
largest_ccs = sorted(nx.connected_component_subgraphs(graph), key=lambda x: len(x))[-1]

h = MatrixPlot(largest_ccs)


h.draw()
plt.show()


for n, d in graph.nodes(data=True):
    graph.node[n]['degree'] = nx.degree(graph,n)
    
# a = ArcPlot(graph=graph, node_order='degree')

# a.draw()
# plt.show()


# Calculate the maximal cliques in G
cliques = nx.find_cliques(graph)

print(len(list(cliques)))



# Find the author(s) that are part of the largest maximal clique
largest_clique = sorted(list(nx.find_cliques(graph)), key=lambda x:len(x))[-1]

G_lc = graph.subgraph(largest_clique)

c = CircosPlot(graph=G_lc)
c.draw()
plt.show()



# Compute the degree centralities of G
deg_cent = nx.degree_centrality(graph)

# Compute the maximum degree centrality
max_dc = max(list(deg_cent.values()))

# Find the user(s) that have collaborated the most: prolific_collaborators
prolific_collaborators = [n for n, dc in deg_cent.items() if dc == deg_cent]





# Identify the largest maximal clique: largest_max_clique
largest_max_clique = set(sorted(nx.find_cliques(graph), key=lambda x: len(x))[-1])

# Create a subgraph from the largest_max_clique
G_lmc = graph.subgraph(largest_max_clique)

# Go out 1 degree of separation
for node in G_lmc.nodes():
    G_lmc.add_nodes_from(graph.neighbors(node))
    G_lmc.add_edges_from(zip([node]*len(graph.neighbors(node)), graph.neighbors(node)))

# Record each node's degree centrality score
for n in G_lmc.nodes():
    G_lmc.node[n]['degree centrality'] = nx.degree_centrality(G_lmc)[n]
        
# a = ArcPlot(G_lmc, node_order='degree centrality')

# a.draw()
# plt.show()




# Initialize the defaultdict
recommended = defaultdict(int)

for n, d in graph.nodes(data=True):
    for n1, n2 in combinations(graph.neighbors(n), 2):
        if not graph.has_edge(n1,n2):
            recommended[(n1, n2)] += 1

# Identify the top 10 pairs of users
all_counts = sorted(recommended.values())
top10_pairs = [pair for pair, count in recommended.items() if count > all_counts[-10]]
print("users who should collaborate: ")
print(top10_pairs)