# HPC_Projet
Projet hpc, simulation d'une epidemie dans un graphe dans un graphe d'un réseau social



## Creation d'un env virtuel
pip install virtualenv

python -m venv HPC_env

HPC_env/Scripts/activate

## Installation des bibliotheques necessaires

pip install -r requirements.txt


## Pour utiliser notre programme
python plotGraphe.py

pour changer le graphe utilisé, regarder ligne 25 et changer la valeur de choice par "congress" ou "facebook"









## Pour mettre les bibliotheques installés dans le fichier requirements.txt
pip freeze > requirements.txt