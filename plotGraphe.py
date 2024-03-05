import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm  # Importer tqdm pour la barre de progression
import numpy as np
from FonctionsUtiles import *
import json

# Définir une fonction pour afficher le graphe avec une barre de progression
def draw_with_progress(graph, layout_function, *args, **kwargs):
    print("Chargement du graphe en cours..")
    fig, ax = plt.subplots()
    pos = layout_function(graph, *args, **kwargs)  # Obtenir la disposition des nœuds
    nx.draw_networkx_nodes(graph, pos=pos, ax=ax, node_size=50, node_color='skyblue')
    nx.draw_networkx_edges(graph, pos=pos, ax=ax)
    plt.axis('off')
    plt.show()



PATHS = "facebook_combined.txt"
PATHS2 = 'web_congress.json'


G = nx.Graph() # Créer un graphe vide
G2 = nx.Graph() # Créer un graphe vide
## Variables importantes
num_lines = sum(1 for line in open(PATHS)) # Compter le nombre de lignes dans le fichier pour obtenir la taille totale de la barre de progression
num_nodes = 4039 # 475 pour congress, 4039 pour web-fb
adj_matrix = [[0] * num_nodes for _ in range(num_nodes)] # Initialiser la matrice d'adjacence avec des zéros
alpha = 1  # Choisissez une valeur pour alpha entre 0 et 1
##

with open(PATHS, "r") as f:
    for line in tqdm(f, total=num_lines, desc="Récupération des données"):  # Utiliser tqdm pour afficher la barre de progression
        node1, node2 = map(int, line.strip().split())
        G.add_edge(node1, node2)
        adj_matrix[node1][node2] = 1
        adj_matrix[node2][node1] = 1

# # Charger les données JSON à partir du fichier
# with open(PATHS2, 'r') as f:
#     data = json.load(f)
# 
# for i, in_nodes in enumerate(data[0]['inList']):
#     for node_id in in_nodes:
#         G.add_edge(node_id, i)  # Ajoutez l'arête entrante
#         adj_matrix[node_id][i] = 1
#         adj_matrix[i][node_id] = 1

# draw_with_progress(G, nx.spring_layout) # Dessiner le graphe

adj_matrix = np.array(adj_matrix)
row_sums = adj_matrix.sum(axis=1)  # Somme des éléments de chaque ligne
transition_matrix = adj_matrix / row_sums[:, np.newaxis]

print("Transition Matrix (P):")
print(transition_matrix)


# Calculer la matrice A
A = alpha * transition_matrix + (1 - alpha) * adj_matrix

# Afficher la matrice A
print("Matrix A:")
print(A)

eigenvalues, eigenvectors = np.linalg.eig(transition_matrix.T)

# Trouver l'index de la valeur propre 1
index = np.where(np.isclose(eigenvalues, 1))[0][0]

# Le vecteur propre correspondant à la valeur propre 1
stationary_distribution = np.real(eigenvectors[:, index])

# Normaliser la distribution stationnaire
stationary_distribution /= stationary_distribution.sum()

# Afficher la distribution stationnaire normalisée
print("Stationary Distribution:")
print(stationary_distribution)

# Exemple d'utilisation
initial_infected = np.random.choice(list(G.nodes()), 1, replace=False)  # Choisissez des nœuds initialement infectés

# Simuler la propagation de l'épidémie avec différentes stratégies de vaccination
# removed_without_vaccination = simulate_epidemic_with_vaccination(G, initial_infected)
# print("Nombre de personnes retirées sans vaccination:", removed_without_vaccination)

vaccinated_with_random_vaccination , removed_with_random_vaccination , dead_with_random_vaccination   = simulate_epidemic_with_vaccination(G, initial_infected, vaccination_strategy='random', vaccination_rate=0.2)
print("Nombre de personnes vaccinées avec vaccination aléatoire: ", vaccinated_with_random_vaccination)
print("Nombre de personnes vaccinées naturellement avec vaccination aléatoire: ", removed_with_random_vaccination)
print("Nombre de personnes mortes avec vaccination aléatoire: ", dead_with_random_vaccination)
print()

# Utilisez le vecteur d'infection issu de l'étape 5 pour la vaccination basée sur le vecteur d'infection
vaccinated_with_infection_vector_vaccination ,removed_with_infection_vector_vaccination, dead_with_infection_vector_vaccination  = simulate_epidemic_with_vaccination(G, initial_infected, vaccination_strategy='infection_vector', vaccination_rate=0.2, infection_vector=stationary_distribution)
print("Nombre de personnes vaccinées avec vaccination basée sur le vecteur d'infection: ", vaccinated_with_infection_vector_vaccination)
print("Nombre de personnes vaccinées naturellement avec vaccination basée sur le vecteur d'infection: ", removed_with_infection_vector_vaccination)
print("Nombre de personnes mortes avec vaccination basée sur le vecteur d'infection: ", dead_with_infection_vector_vaccination)
print()




