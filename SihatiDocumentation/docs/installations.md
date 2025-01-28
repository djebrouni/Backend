
## Prérequis

Avant de commencer l'installation, assurez-vous que vous disposez des outils suivants installés sur votre machine :

- **Python** (version 3.8 ou supérieure) : [Télécharger Python](https://www.python.org/downloads/)
- **pip** (gestionnaire de paquets Python) : Il est normalement inclus avec Python.
- **Git** (si vous clonez le projet depuis GitHub) : [Télécharger Git](https://git-scm.com/downloads)
- **Base de données** : Ce projet utilise une base de données relationnelle (par défaut SQLite). Vous pouvez également configurer d'autres bases de données comme PostgreSQL ou MySQL si nécessaire.

## Étapes d'Installation
1. Clonez le projet depuis GitHub :

   ```bash
   git clone https://github.com/ton-projet.git

2.Installez les dépendances :

bash
Copier le code :
pip install -r requirements.txt

3.Effectuez les migrations de la base de données :

bash
Copier le code:
python manage.py migrate

4.Lancez le serveur de développement :

bash
Copier le code:
python manage.py runserver
Vous pouvez maintenant accéder à l'application à l'adresse http://127.0.0.1:8000.