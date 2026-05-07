# Installation

## Prérequis

- [Python 3.10+](https://www.python.org/downloads/) — lors de l'installation, coche bien **"Add Python to PATH"**
- [Git](https://git-scm.com/download/win)

---

## Étapes

### 1. Télécharger le projet

```bash
git clone https://github.com/ton-user/ton-repo.git
cd ton-repo
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer l'application

```bash
python main.py
```

---

## Problèmes fréquents

**`python` n'est pas reconnu** → essaie `python3` à la place, ou réinstalle Python en cochant "Add to PATH".

**Erreur à l'activation du venv** → ouvre PowerShell en administrateur et tape :
```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Puis réessaie `.venv\Scripts\activate`.

**Erreur à l'import de PySide6** → vérifie que tu vois bien `(.venv)` au début de ta ligne de commande avant de lancer `pip install`.
