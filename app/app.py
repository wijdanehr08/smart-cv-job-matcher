import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from preprocessing.text_cleaning import clean_text, extract_text_from_pdf
from matching.similarity import JobMatcher

# --- Configuration de la page Streamlit ---
st.set_page_config(
    page_title="Smart CV Analyzer & Job Matcher",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for a professional look ---
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #ffffff;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #262730;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stSuccess {
        background-color: #e6ffe6;
        color: #006600;
        border-left: 5px solid #00cc00;
        padding: 10px;
        border-radius: 5px;
    }
    .stWarning {
        background-color: #fff3e6;
        color: #cc6600;
        border-left: 5px solid #ff9900;
        padding: 10px;
        border-radius: 5px;
    }
    .stInfo {
        background-color: #e6f7ff;
        color: #0066cc;
        border-left: 5px solid #0099ff;
        padding: 10px;
        border-radius: 5px;
    }
    .block-container { 
        padding-top: 2rem; 
        padding-bottom: 0rem; 
        padding-left: 5rem; 
        padding-right: 5rem; 
    }
    .css-1d391kg {
        padding-top: 3.5rem;
        padding-right: 1rem;
        padding-bottom: 3.5rem;
        padding-left: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialisation du JobMatcher (chargement du modèle Transformer) ---
@st.cache_resource
def load_job_matcher():
    return JobMatcher()

job_matcher = load_job_matcher()

# --- Fonctions d'affichage ---
def display_score(score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {"x": [0, 1], "y": [0, 1]},
        title = {"text": "Score de Correspondance", "font": {"size": 24, "color": "#262730"}},
        gauge = {
            "axis": {"range": [None, 100], "tickwidth": 1, "tickcolor": "#262730"},
            "bar": {"color": "#2a9d8f"},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "gray",
            "steps": [
                {"range": [0, 20], "color": "#e76f51"},
                {"range": [20, 40], "color": "#f4a261"},
                {"range": [40, 60], "color": "#e9c46a"},
                {"range": [60, 80], "color": "#2a9d8f"},
                {"range": [80, 100], "color": "#264653"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": score
            }
        }
    ))
    fig.update_layout(height=250, margin=dict(l=10, r=10, t=50, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

def display_skills_feedback(matched_skills, missing_skills):
    st.subheader("Feedback Détaillé sur les Compétences")
    
    if matched_skills:
        st.success(f"**Compétences Correspondantes :** {', '.join([s.title() for s in matched_skills])}")
    else:
        st.info("Aucune compétence clé directement correspondante trouvée dans les deux documents.")

    if missing_skills:
        st.warning(f"**Compétences Manquantes dans votre CV (présentes dans l'offre) :** {', '.join([s.title() for s in missing_skills])}")
        st.info("Considérez à inclure ces compétences dans votre CV si vous les possédez ou si vous avez une expérience pertinente.")
    else:
        st.success("Votre CV semble couvrir toutes les compétences clés de l'offre !")

    # Visualisation des compétences
    if matched_skills or missing_skills:
        skills_data = {
            'Compétence': [s.title() for s in matched_skills] + [s.title() for s in missing_skills],
            'Statut': ['Correspondante'] * len(matched_skills) + ['Manquante'] * len(missing_skills),
            'Count': [1] * (len(matched_skills) + len(missing_skills))
        }
        df_skills = pd.DataFrame(skills_data)

        if not df_skills.empty:
            st.markdown("### Visualisation des Compétences")
            fig_skills = px.bar(
                df_skills,
                y='Compétence',
                x='Count',
                color='Statut',
                orientation='h',
                title='Analyse des Compétences Clés',
                color_discrete_map={'Correspondante': '#2a9d8f', 'Manquante': '#e76f51'},
                height=max(400, len(df_skills) * 30)
            )
            fig_skills.update_layout(showlegend=True, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_skills, use_container_width=True)

# --- Interface Utilisateur Streamlit ---
st.title("🧠 Smart CV Analyzer & Job Matcher")
st.markdown("""
    <p style='font-size: 1.2em; color: #555;'>
        Optimisez votre CV avec l'intelligence artificielle pour décrocher le poste de vos rêves.
    </p>
""", unsafe_allow_html=True)
st.markdown("---", unsafe_allow_html=True)

st.sidebar.header("À Propos")
st.sidebar.info(
    "Cette application utilise l'IA pour analyser sémantiquement votre CV et une offre d'emploi, "
    "fournissant un score de correspondance et un feedback détaillé sur les compétences. "
    "Conçu pour les profils IA, Data, Cloud & Cyber !"
)

# --- Entrée CV et Offre d'Emploi ---
col1, col2 = st.columns(2)

with col1:
    st.header("Votre CV")
    cv_option = st.radio("Comment souhaitez-vous fournir votre CV ?", ("Coller le texte", "Uploader un PDF"), key="cv_option")
    cv_text = ""
    if cv_option == "Coller le texte":
        cv_text = st.text_area("Collez le texte de votre CV ici :", height=350, key="cv_text_area",
                               placeholder="Ex: Expérience: Développeur Python, Compétences: Machine Learning, SQL...")
    elif cv_option == "Uploader un PDF":
        uploaded_file = st.file_uploader("Uploader votre CV au format PDF", type=["pdf"], key="cv_pdf_uploader")
        if uploaded_file is not None:
            try:
                cv_text = extract_text_from_pdf(uploaded_file)
                st.success("PDF du CV extrait avec succès !")
            except Exception as e:
                st.error(f"Erreur lors de l'extraction du PDF : {e}")

with col2:
    st.header("Offre d'Emploi / Stage")
    job_description = st.text_area("Collez le texte de l'offre d'emploi ou de stage ici :", height=350, key="job_text_area",
                                   placeholder="Ex: Nous recherchons un Data Scientist avec expérience en Python, TensorFlow, AWS...")

# --- Bouton d'Analyse ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Analyser la Correspondance", type="primary"):
    if cv_text and job_description:
        with st.spinner("Analyse sémantique en cours... Préparation de votre feedback personnalisé."):
            cleaned_cv = clean_text(cv_text)
            cleaned_job = clean_text(job_description)

            if not cleaned_cv or not cleaned_job:
                st.error("Veuillez fournir du texte valide pour le CV et l'offre d'emploi après nettoyage.")
            else:
                # Calcul du score de similarité sémantique
                similarity_score = job_matcher.match(cleaned_cv, cleaned_job)
                
                # Extraction des compétences pour le feedback
                matched_skills, missing_skills = job_matcher.extract_keywords_match(cleaned_cv, cleaned_job)

                st.success("Analyse terminée avec succès !")
                st.markdown("## Résultats Détaillés de la Correspondance")
                
                col_score, col_metric = st.columns([0.7, 0.3])
                with col_score:
                    display_score(similarity_score)
                with col_metric:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.metric(label="Score de Similarité Sémantique", value=f"{similarity_score}%")
                    st.info("Ce score représente la similarité contextuelle entre votre CV et l'offre. Un score élevé indique une forte adéquation sémantique.")

                st.markdown("---", unsafe_allow_html=True)
                display_skills_feedback(matched_skills, missing_skills)

                st.markdown("---", unsafe_allow_html=True)
                st.subheader("💡 Conseils Personnalisés pour Optimiser votre CV")
                st.markdown(
                    "*   **Adaptez votre CV** : Mettez en évidence les compétences et expériences les plus pertinentes pour chaque offre. Ne laissez rien au hasard !"
                    "*   **Intégrez les mots-clés** : Utilisez les termes exacts de l'offre d'emploi, surtout pour les compétences techniques. Les ATS (Applicant Tracking Systems) les recherchent."
                    "*   **Quantifiez vos réalisations** : Au lieu de dire 'J'ai géré des projets', dites 'J'ai géré 5 projets, réduisant les coûts de 15%'. Les chiffres parlent !"
                    "*   **Structure claire et professionnelle** : Un CV bien organisé et facile à lire fait une excellente première impression. Pensez à la lisibilité !"
                    "*   **Développez les compétences manquantes** : Si des compétences clés sont identifiées comme manquantes, envisagez des formations ou des projets personnels pour les acquérir."
                )

    else:
        st.error("Veuillez coller le texte de votre CV et de l'offre d'emploi, ou uploader un PDF pour le CV, avant de lancer l'analyse.")


# --- Footer ---
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f0f2f6;
    color: #555;
    text-align: center;
    padding: 10px;
    font-size: 12px;
    border-top: 1px solid #e0e0e0;
}

""", unsafe_allow_html=True)
