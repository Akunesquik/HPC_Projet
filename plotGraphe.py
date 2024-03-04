import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm  # Importer tqdm pour la barre de progression

# Définir une fonction pour afficher le graphe avec une barre de progression
def draw_with_progress(graph, layout_function, *args, **kwargs):
    fig, ax = plt.subplots()
    pos = layout_function(graph, *args, **kwargs)  # Obtenir la disposition des nœuds
    nx.draw_networkx_nodes(graph, pos=pos, ax=ax, node_size=50, node_color='skyblue')
    nx.draw_networkx_edges(graph, pos=pos, ax=ax)
    plt.axis('off')
    plt.show()

# Créer un graphe vide
G = nx.Graph()

# Compter le nombre de lignes dans le fichier pour obtenir la taille totale de la barre de progression
num_lines = sum(1 for line in open("web-fb.txt"))

# Lire les données du fichier et ajouter les arêtes au graphe
with open("web-fb.txt", "r") as f:
    for line in tqdm(f, total=num_lines, desc="Loading graph"):  # Utiliser tqdm pour afficher la barre de progression
        node1, node2 = map(int, line.strip().split())
        G.add_edge(node1, node2)

# Afficher le graphe avec une barre de progression
draw_with_progress(G, nx.spring_layout)
