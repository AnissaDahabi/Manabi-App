# 学 Manabi App

Application de bureau Python permettant aux administrateurs et professeurs de gérer les cours de japonais, les sessions, les utilisateurs et les réservations.

> Client lourd du projet Manabi : le client léger (web) est dédié aux élèves pour consulter et réserver des cours.

---

## Fonctionnalités

- Authentification par e-mail / mot de passe avec gestion des rôles (administrateur / professeur)
- Tableau de bord présentant des statistiques globales de la plateforme
- Gestion complète des utilisateurs (création, modification, suppression) : réservée aux administrateurs
- Gestion des cours et sessions : les administrateurs accèdent à l'ensemble des données, les professeurs uniquement aux cours et sessions qui leur sont attribués
- Gestion des réservations (confirmation, annulation, affichage) : réservée aux administrateurs
- Interface stylisée en QSS, cohérente visuellement avec l'application web Manabi

---

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Langage | Python |
| Interface graphique | PySide6 |
| Stylisation | QSS |
| Base de données | MySQL |
| Accès BDD | mysql-connector-python avec requêtes préparées |
| Architecture | Couches séparées (modèles / services / pages GUI) |
| IDE | PyCharm |
| Versionning | Git / GitHub |

---

## Démo

Pour tester l'application, utilisez les comptes suivants :

### Administrateur

| Champ | Valeur |
|-------|--------|
| E-mail | sophie.moreau@manabi.com |
| Mot de passe | admin123 |

### Professeur

| Champ | Valeur |
|-------|--------|
| E-mail | hiroshi.tanaka@manabi.com |
| Mot de passe | prof1234 |

---

## Structure du projet

```
manabi-app/
├── main.py
├── config/
│   └── database.py
├── models/
│   ├── user.py
│   ├── cours.py
│   ├── session.py
│   └── reservation.py
├── services/
│   ├── auth_service.py
│   ├── user_service.py
│   ├── cours_service.py
│   ├── session_service.py
│   └── reservation_service.py
├── pages/
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── users_page.py
│   ├── cours_page.py
│   ├── sessions_page.py
│   └── reservations_page.py
└── assets/
    ├── style.qss
    └── images/
        └── logo.png
```

---

## Installation

### Prérequis

- [Python 3.10+](https://www.python.org/downloads/) — lors de l'installation, coche bien **"Add Python to PATH"**
- [Git](https://git-scm.com/download/win)

---

### Étapes

#### 1. Télécharger le projet

```bash
git clone https://github.com/ton-user/ton-repo.git
cd ton-repo
```

#### 2. Créer un environnement virtuel

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

#### 4. Lancer l'application

```bash
python main.py
```

---

### Problèmes fréquents

**`python` n'est pas reconnu** → essaie `python3` à la place, ou réinstalle Python en cochant "Add to PATH".

**Erreur à l'activation du venv** → ouvre PowerShell en administrateur et tape :
```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Puis réessaie `.venv\Scripts\activate`.

**Erreur à l'import de PySide6** → vérifie que tu vois bien `(.venv)` au début de ta ligne de commande avant de lancer `pip install`.
