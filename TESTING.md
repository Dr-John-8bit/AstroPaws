# 🧪 Guide de test pour AstroPaws

Ce fichier explique comment **tester le jeu AstroPaws** sans connaissance en programmation, sur **macOS (puce Apple Silicon)** et **Ubuntu**.

---

## 🍎 Tester sur macOS (Apple Silicon) avec Visual Studio Code

### 1. Installer Python

- Va sur [https://www.python.org/downloads/macos/](https://www.python.org/downloads/macos/)
- Télécharge et installe **Python 3.x** via l’installeur `.pkg`
- Vérifie que Python est installé :  
  Ouvre le Terminal et tape :
  ```bash
  python3 --version
  ```

### 2. Installer Visual Studio Code

- Va sur [https://code.visualstudio.com/](https://code.visualstudio.com/)
- Télécharge et installe **Visual Studio Code pour Mac**

Ouvre VS Code et installe l’extension **Python** (via l’onglet Extensions à gauche).

### 3. Télécharger AstroPaws

- Ouvre Visual Studio Code
- Menu `Fichier > Ouvrir un dossier…` puis sélectionne un dossier pour y placer le jeu
- Ouvre le Terminal intégré (`Ctrl + `` ou `Affichage > Terminal`)
- Copie-colle :
  ```bash
  git clone https://github.com/Dr-John-8bit/AstroPaws.git
  cd AstroPaws
  ```

### 4. Installer les dépendances

Dans le terminal intégré :
```bash
python3 -m pip install -r requirements.txt
```

### 5. Lancer le jeu

Toujours dans le terminal intégré :
```bash
python3 main.py
```

Le jeu se lance dans une fenêtre séparée. Utilise les flèches, Espace, `P`, `J`, etc. pour jouer (voir [MANUAL.md](MANUAL.md)).

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