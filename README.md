# 🚗 Projet de Prédiction d'Occupation de Parking

## 📖 Description du Projet
Ce projet utilise des algorithmes d'apprentissage automatique (Machine Learning) pour estimer le niveau d'occupation de différents parkings. Le but est de prédire le nombre de places occupées en fonction de plusieurs facteurs tels que l'heure de la journée, le jour de la semaine et la capacité du parking. 

Le projet inclut à la fois la partie "Science des Données" (nettoyage, exploration et entraînement du modèle) et une application web interactive permettant aux utilisateurs de simuler des prédictions en temps réel.

---

## 🛠️ Outils et Technologies Utilisés

Ce projet s'appuie sur plusieurs bibliothèques standards de l'écosystème Python :

- **Python 3** : Le langage de programmation principal.
- **Scikit-Learn** : Bibliothèque de Machine Learning. Utilisée ici pour créer, entraîner et évaluer notre modèle prédictif basé sur l'algorithme des **Forêts Aléatoires** (*Random Forest*).
- **Pandas & NumPy** : Outils indispensables pour la manipulation de la donnée. Ils ont permis de charger les fichiers, de traiter les valeurs aberrantes, et d'appliquer le *One-Hot Encoding* sur les noms de parkings.
- **Streamlit** : Un framework Python très puissant utilisé pour développer l'interface utilisateur web interactive (`dashboard.py`) de manière simple et rapide.
- **Jupyter Notebook** : L'environnement de développement utilisé pour la phase de recherche, les expérimentations et la visualisation des données (`code.ipynb`).
- **Joblib** : Utilisé pour sérialiser et sauvegarder le modèle prédictif une fois l'entraînement terminé, afin qu'il puisse être réutilisé instantanément par le tableau de bord sans nécessiter un nouvel entraînement.

---

## 📁 Architecture du Projet

```text
projet_prediction_parking/
│
├── data/           # Dossier contenant les données (CSV)
├── models/         # Dossier contenant  le modèle sauvegardé (joblib)
├── notebook/       # Dossier d'expérimentation (Data Science)
│   └── code.ipynb  # Notebook contenant le nettoyage des données et l'entraînement du modèle
├── Scripts/        # Dossier contenant le code de l'application finale
│   └── dashboard.py# Le script de l'application web Streamlit
└── README.md       # Ce fichier de documentation
```

---

## 🚀 Comment lancer le projet en local ?

### 1. Prérequis
Assurez-vous d'avoir Python installé sur votre machine, puis installez les dépendances nécessaires en tapant cette commande dans votre terminal :

```bash
pip install streamlit pandas scikit-learn numpy joblib
```

### 2. (Optionnel) Entraîner le Modèle
Si vous souhaitez réentraîner le modèle avec de nouvelles données, ouvrez le fichier `notebook/code.ipynb` via Jupyter, exécutez toutes les cellules. Un nouveau fichier `meilleur_modele_prediction_occupation.joblib` sera alors généré dans le dossier `data/`.

### 3. Lancer le Tableau de Bord
Ouvrez un terminal à la racine du projet (le dossier `projet_prediction_parking`) et exécutez la commande suivante :

```bash
streamlit run Scripts/dashboard.py
```

L'application s'ouvrira automatiquement dans votre navigateur web (généralement à l'adresse `http://localhost:8501`).

---

## 🧠 Fonctionnement de l'Interface

Une fois l'application lancée, l'utilisateur a accès à plusieurs paramètres :
1. **Sélection du parking** : Grâce au traitement *One-Hot Encoding*, le modèle reconnaît chaque parking indépendamment.
2. **Capacité totale** : Pour ajuster la taille du parking.
3. **L'heure et le jour** : Des curseurs et menus déroulants permettent de choisir une heure (0h-23h) et un jour de la semaine.

En cliquant sur **Effectuer la prédiction**, l'application interroge le modèle Random Forest sauvegardé et affiche :
- Le nombre exact de places qui risquent d'être occupées.
- Une barre de progression colorée dynamique calculant le taux de remplissage (Vert si libre, Orange si moyennement occupé, Rouge si critique).
