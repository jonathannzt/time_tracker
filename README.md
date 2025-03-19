# Time Tracker

Ce projet permet de suivre le **temps passé** sur chaque application (processus) Windows, de sauvegarder les données dans une base SQLite, et de générer des rapports **graphiques** via une interface Tkinter. C'est un projet personnel 

## Fonctionnalités

1. **Suivi du temps** par application :  
   - Détection du process actif (ex.: `chrome.exe`) grâce à `win32gui` et `psutil`.
   - Sauvegarde continue dans une base SQLite (chaque session de début/fin).

2. **Interface graphique** (Tkinter) :  
   - Démarrer / Arrêter le tracking.
   - Affichage en temps réel du temps cumulé par application.
   - Bouton pour générer un **camembert** (ou pie chart) de la répartition du temps.

3. **Sauvegarde persistante** (SQLite) :  
   - Toutes les sessions sont archivées dans `time_tracker.db`.  
   - Possibilité de faire des requêtes plus fines (par date, par application, etc.).

4. **Fichier de configuration** (`config.json`) :  
   - Personnaliser l’**intervalle de tracking** (en secondes) et l’**intervalle de rafraîchissement** de l’interface (en millisecondes).  
   - Créé automatiquement s’il n’existe pas encore.

## Structure du projet

- **time_tracker/**
  - **main.py**  
    Point d’entrée principal.  
    - Charge la configuration (`config.json`).  
    - Crée l’instance de `TimeTracker`.  
    - Lance l’interface `App`.

  - **requirements.txt**  
    Liste des dépendances à installer.

  - **README.md**  
    Documentation générale du projet.

  - **src/**
    - **tracker.py**  
      Classe `TimeTracker` gérant le suivi du temps.  
      - Récupère la fenêtre active (processus) à intervalles réguliers.  
      - Insère les sessions (début/fin) dans la base SQLite via `DatabaseManager`.

    - **gui.py**  
      Classe `App` (héritée de `tk.Tk`) gérant l’interface utilisateur.  
      - Affiche la liste des applications et le temps cumulé.  
      - Propose un bouton pour tracer un diagramme à l’aide de `matplotlib`.

    - **database.py**  
      Classe `DatabaseManager` qui gère la création de la table `activities` et les insertions/requêtes (somme du temps par application, etc.).

    - **config.py**  
      Gère le chargement/sauvegarde d’un fichier `config.json`.  
      - Permet de définir (et de modifier facilement) des paramètres comme :  
        - `update_interval` : Intervalle (en secondes) de détection de la fenêtre active.  
        - `refresh_interval` : Intervalle (en millisecondes) de rafraîchissement de l’interface.

## Installation & Lancement

1. **Cloner** ce dépôt ou téléchargez les fichiers.  
2. Placez-vous dans le dossier `time_tracker` et installez les dépendances :
   ```bash
   pip install -r requirements.txt