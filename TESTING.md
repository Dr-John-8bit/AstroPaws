# 🧪 Guide de test pour AstroPaws

Ce fichier explique comment **tester le jeu AstroPaws** sans connaissance en programmation, sur **macOS (puce Apple Silicon)** et **Ubuntu**.

---

## 🍎 Tester sur macOS (Apple Silicon) avec Visual Studio Code

### 1. Installer Python 3

- Va sur [https://www.python.org/downloads/macos/](https://www.python.org/downloads/macos/)
- Télécharge et installe **Python 3.x** via l’installeur `.pkg` (version universelle recommandée)
- Ouvre le Terminal et tape pour vérifier :
  ```bash
  python3 --version
  ```

### 2. Installer Visual Studio Code

- Va sur [https://code.visualstudio.com/](https://code.visualstudio.com/)
- Télécharge et installe **Visual Studio Code pour Mac**
- Ouvre VS Code et installe l’extension **Python** depuis l’onglet Extensions (ou tape `Ctrl+Shift+X` et cherche "Python")

### 3. Télécharger AstroPaws

- Ouvre VS Code
- Menu `Fichier > Ouvrir un dossier…` et choisis un dossier de travail
- Ouvre le terminal intégré via `Affichage > Terminal` ou `Ctrl + \``
- Clone le projet :
  ```bash
  git clone https://github.com/Dr-John-8bit/AstroPaws.git
  cd AstroPaws
  ```

### 4. Installer les dépendances

Dans le terminal intégré :
```bash
python3 -m pip install pygame
```

Si vous voyez une erreur comme `ModuleNotFoundError: No module named 'pygame'`, cela signifie que cette étape n’a pas été faite correctement.

### 5. Lancer le jeu

Deux méthodes sont possibles :

#### 🟢 Depuis le terminal intégré :
```bash
python3 main.py
```

#### 🟣 Depuis Visual Studio Code (interactif) :
- Ouvre le fichier `main.py` dans VS Code
- Appuie sur `F5` pour lancer en mode exécution
- Ou clique sur la flèche verte ▶️ en haut à droite de l'éditeur

Le jeu s’ouvre dans une fenêtre dédiée. Utilise les touches fléchées, Espace, `P`, `I`, `J`, etc. (voir [MANUAL.md](MANUAL.md) pour le détail des commandes).

---

## 🐧 Tester sur Ubuntu

### 1. Installer Python 3 et pip

Ouvre un Terminal et tape :
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 2. Télécharger le jeu

```bash
git clone https://github.com/Dr-John-8bit/AstroPaws.git
cd AstroPaws
```

### 3. Installer les dépendances

```bash
pip3 install -r requirements.txt
```

### 4. Lancer le jeu

```bash
python3 main.py
```

---

## 🛟 Besoin d’aide ?

Si le jeu ne se lance pas ou que tu rencontres une erreur :
- Vérifie que tu es bien dans le dossier `AstroPaws`
- Vérifie que Python est bien installé
- Tu peux créer une "Issue" sur GitHub ou contacter Dr John 8bit pour de l’aide.

---