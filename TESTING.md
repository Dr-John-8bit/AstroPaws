


# 🧪 Guide de test pour AstroPaws

Ce fichier explique comment **tester le jeu AstroPaws** sans connaissance en programmation, sur **macOS (puce Apple Silicon)** et **Ubuntu**.

---

## 🍎 Tester sur macOS (Apple Silicon)

### 1. Installer Python 3

- Va sur [https://www.python.org/downloads/macos/](https://www.python.org/downloads/macos/)
- Télécharge et installe la dernière version de **Python 3.x** (installeur `.pkg`)
- Vérifie l'installation :  
  Ouvre le Terminal et tape :
  ```bash
  python3 --version
  ```

### 2. Télécharger le jeu

Dans le Terminal :
```bash
git clone https://github.com/Dr-John-8bit/AstroPaws.git
cd AstroPaws
```

### 3. Installer les dépendances

Toujours dans le Terminal :
```bash
python3 -m pip install -r requirements.txt
```

### 4. Lancer le jeu

```bash
python3 main.py
```

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