Ce projet vise à récupérer les articles du fournisseur Béligné et automatiser la création vers une boutique Prestashop. Il comporte une partie de création et utilisation d'un modèle de langage pour automatiser la catégorisation des articles.

## Table des matières

- Prérequis
- Installation
- Configuration
- Utilisation
  - Scrapping
  - Catégorisation
- Structure du projet
- Modèles et IA

## Prérequis

- Python 3.8+
- [Ollama](https://ollama.ai/) installé localement pour les fonctionnalités de catégorisation
- Un compte sur le site Béligné Pro

## Installation

1. Clonez ce dépôt

```shell
$ git clone <url-du-repo>
```

2. Installez les dépendances

```shell
$ pip install -r requirements.txt
```

## Configuration

1. Créez un fichier .env à la racine du projet

```shell
$ touch .env
```

2. Ajoutez les informations suivantes dans le fichier .env

```
EMAIL=email_de_connexion
PASSWORD=mot_de_passe
OLLAMA_BASE_URL=http://localhost:11434/api/
```

3. Assurez-vous que Ollama est en cours d'exécution sur votre machine locale

```shell
$ ollama serve  # Si pas déjà lancé en tant que service
```

## Utilisation

### Affichage des arguments disponibles

```shell
$ python main.py --help
```

### Scrapping

Pour récupérer les données des articles à partir d'une liste de références :

```shell
$ python main.py --mode scrap --sinput 'chemin_vers_la_priceList'
```

Le fichier priceList doit être au format CSV avec une colonne "ref" contenant les références des produits à scraper.

### Catégorisation

**En cours de création**

Pour catégoriser automatiquement les articles précédemment scrapés :

```shell
$ python main.py --mode categorize
```

Cette commande utilisera le modèle de langage configuré avec Ollama pour analyser les articles dans data.csv et proposer des catégories appropriées.

## Structure du projet

- main.py - Point d'entrée principal du programme
- tools - Modules utilitaires
  - scrapper.py - Fonctions pour le scraping des données
  - categorizer.py - Fonctions pour la catégorisation des articles
  - dataFormatter.py - Outils de traitement des données
  - ollamaAPI.py - Interface avec l'API Ollama
- data - Répertoire contenant les fichiers de données
- downloaded_images - Dossier où sont stockées les images téléchargées
- ModelFiles - Configurations de modèles pour Ollama

## Modèles et IA

Ce projet utilise des modèles de langage via l'API Ollama pour la catégorisation automatique des produits. Le modèle principal est défini dans DeepseekCreateClassifier.json et est basé sur deepseek-r1:7b.
