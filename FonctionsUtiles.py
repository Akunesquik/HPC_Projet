import copy
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from IPython.display import clear_output

def simulate_epidemic_with_vaccination(graph, initial_infected, vaccination_strategy=None, vaccination_rate=0, infection_vector=None):
    # Créer une copie du graphe original pour simuler la propagation de l'épidémie
    current_graph = copy.deepcopy(graph)
    infected = set(initial_infected)
    susceptible = set(graph.nodes()) - infected
    vaccinated = set()
    removed = set()
    dead = set()
    # Probabilité d'infection lors d'un contact avec un nœud infecté
    infection_probability = 0.1
    vaccination_probability = 0.05
    recup_probability = 0.05
    death_probability = 0.1
    # Ajouter un attribut 'state' à chaque nœud pour suivre son état (sain, infecté, retiré, vacciné)
    for node in current_graph.nodes():
        if node in infected:
            current_graph.nodes[node]['state'] = 'infected'
        elif node in susceptible:
            current_graph.nodes[node]['state'] = 'susceptible'
        else:
            current_graph.nodes[node]['state'] = 'removed'
    
    # Fonction pour propager l'épidémie d'un nœud infecté à ses voisins
    def spread_infection(node):
        nonlocal infected, susceptible
        neighbors = set(current_graph.neighbors(node))
        for neighbor in neighbors:
            if neighbor in susceptible:
                if np.random.random() < infection_probability:
                    infected.add(neighbor)
                    susceptible.remove(neighbor)
                    current_graph.nodes[neighbor]['state'] = 'infected'
    
    # Fonction pour effectuer la vaccination en fonction de la stratégie choisie
    def vaccinate_nodes():
        nonlocal susceptible
        if not susceptible:
            return  # Arrêtez la fonction si aucun nœud susceptible n'est disponible
        if vaccination_strategy == 'random':
            # Créez une copie de l'ensemble susceptible pour itérer
            susceptible_copy = set(susceptible)
            for node in susceptible_copy:
                if np.random.rand() < vaccination_probability:  # Comparer la probabilité avec un nombre aléatoire
                    susceptible.remove(node)  # Retirer le nœud de l'ensemble des nœuds susceptibles
                    vaccinated.add(node)
                    current_graph.nodes[node]['state'] = 'vaccinated'  # Mettre à jour l'état du nœud
        elif vaccination_strategy == 'infection_vector':
            # Vacciner les nœuds les plus importants selon le vecteur d'infection
            sorted_indices = np.argsort(infection_vector)[::-1]  # Trier les indices du vecteur d'infection dans l'ordre décroissant
            num_to_vaccinate = int(len(graph.nodes()) * vaccination_rate)
            vaccinated_nodes = sorted_indices[:num_to_vaccinate]
            susceptible -= set(vaccinated_nodes)
            for node in vaccinated_nodes:
                current_graph.nodes[node]['state'] = 'vaccinated'
    
    plt.ion()  # Activer le mode interactif de Matplotlib
    fig = plt.figure()
     # Créer une disposition initiale des nœuds
    initial_pos = nx.spring_layout(current_graph)
    # Simulation de la propagation de l'épidémie
    i = 0
    while infected:
        for node in list(infected):
            spread_infection(node)
            if np.random.random() < recup_probability:  # Taux de récupération arbitraire
                infected.remove(node)
                removed.add(node)
                current_graph.nodes[node]['state'] = 'removed'
            elif np.random.random() < death_probability:  # taux de mort
                infected.remove(node)
                dead.add(node)
                current_graph.nodes[node]['state'] = 'dead'
        vaccinate_nodes()
        
        # Affichage du graphe à chaque étape de la simulation
        state_colors = {'susceptible': 'skyblue', 'infected': 'red', 'removed': 'limegreen', 'vaccinated': 'green', 'dead': 'grey'}
        plt.clf()
        node_colors = [state_colors[current_graph.nodes[node]['state']] for node in current_graph.nodes()]
        nx.draw_networkx_nodes(current_graph, pos=initial_pos, node_color=node_colors, node_size=100)
        nx.draw_networkx_edges(current_graph, pos=initial_pos)
        plt.title("Étape de la simulation")
        plt.axis('off')
        plt.show()
        if i > 10:
            plt.pause(0.5)
        else: 
            plt.pause(2)
        i += 1
        
        
    
    return len(vaccinated), len(removed) , len(dead)