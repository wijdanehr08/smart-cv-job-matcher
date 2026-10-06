# 🧠 Smart CV Analyzer & Job Matcher

Optimisez votre CV avec l'intelligence artificielle pour décrocher le poste de vos rêves.

## 📋 À propos

Cette application utilise l'IA pour analyser sémantiquement votre CV et une offre d'emploi, en fournissant un score de correspondance et un feedback détaillé sur les compétences. Conçu pour les profils IA, Data, Cloud & Cyber !

## ✨ Fonctionnalités

- **Analyse sémantique** du CV et de l'offre d'emploi via des embeddings (Sentence Transformers)
- **Score de correspondance** basé sur la similarité contextuelle
- **Détection automatique des compétences** présentes et manquantes (100+ compétences)
- **Visualisation interactive** des résultats (jauge de score, graphiques de compétences)
- Upload de CV au format **PDF** ou saisie de texte brut

## 🛠️ Stack technique

- **Python**
- **Streamlit** – interface utilisateur
- **Sentence Transformers** – embeddings et similarité sémantique
- **NLP** – extraction et traitement de texte

## 🚀 Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/wijdanehr08/smart-cv-job-matcher.git
cd smart-cv-job-matcher
```

2. Créez et activez un environnement virtuel :
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## ▶️ Utilisation

```bash
streamlit run app/app.py
```

Puis ouvrez votre navigateur à l'adresse indiquée (généralement `http://localhost:8501`).

1. Uploadez votre CV (PDF) ou collez son contenu
2. Collez le texte de l'offre d'emploi
3. Cliquez sur **"Analyser la Correspondance"**
4. Consultez votre score de correspondance et les compétences à ajouter
