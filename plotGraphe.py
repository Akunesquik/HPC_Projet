import networkx as nx
import matplotlib.pyplot as plt

# Créer un graphe vide
G = nx.Graph()

# Lire les données du fichier et ajouter les arêtes au graphe
with open("web-fb.txt", "r") as f:
    for line in f:
        node1, node2 = map(int, line.strip().split())
        G.add_edge(node1, node2)

# Plot the graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)  # Définir la disposition des noeuds
nx.draw(G, pos, node_size=50, node_color='skyblue', with_labels=False)
plt.title("Graph from web-fb.txt")
plt.show()
