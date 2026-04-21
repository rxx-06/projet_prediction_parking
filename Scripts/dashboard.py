import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

# Configuration de l'apparence de la page
st.set_page_config(page_title="Prédiction Parking", page_icon="🚗", layout="centered")

st.title("🚗 Tableau de Bord : Prédiction d'Occupation")
st.markdown("Ce tableau de bord utilise votre modèle de Machine Learning (Random Forest) "
            "pour estimer le nombre de places occupées dans un parking.")

# 1. Fonction pour charger le modèle entrainé
@st.cache_resource
def load_model():
    # S'assurer que le chemin est correct selon d'où le ficher est lancé
    chemin_modele = os.path.join("data", "meilleur_modele_prediction_occupation.joblib")
    return joblib.load(chemin_modele)

try:
    model = load_model()
    st.success("Modèle Machine Learning chargé avec succès ! ✅")
except Exception as e:
    st.error(f"Erreur : Impossible de trouver le modèle. Avez-vous bien généré le fichier 'meilleur_modele_prediction_occupation.joblib' dans le dossier data ?\n\nErreur technique : {e}")
    st.stop()

# 2. Interface utilisateur (Sliders et Menus)
st.markdown("---")
st.subheader("Entrez les paramètres du parking :")

# Extraction automatique des noms de parkings à partir du modèle entrainé
expected_features = model.feature_names_in_
parking_list = [col.replace('SystemCodeNumber_', '') for col in expected_features if col.startswith('SystemCodeNumber_')]

col_park, col_cap = st.columns(2)
with col_park:
    parking_choisi = st.selectbox("📍 Sélectionnez le Parking", options=parking_list)
with col_cap:
    capacite = st.number_input("🅿️ Capacité totale du parking", min_value=10, max_value=5000, value=500, step=10)

col1, col2 = st.columns(2)
with col1:
    heure = st.slider("🕒 Heure de la journée (0h-23h)", min_value=0, max_value=23, value=14, step=1)
with col2:
    jours_semaine = {0: "Lundi", 1: "Mardi", 2: "Mercredi", 3: "Jeudi", 4: "Vendredi", 5: "Samedi", 6: "Dimanche"}
    jour_choisi = st.selectbox("📅 Ce sera quel jour ? ", options=list(jours_semaine.keys()), format_func=lambda x: jours_semaine[x])

# 3. Traitement au clic du bouton
if st.button("🔮 Effectuer la prédiction", type="primary", use_container_width=True):
    
    # Construction du tableau de données (DataFrame) pour le modèle
    # Le modèle attend désormais toutes vos colonnes (Hour, DayOfWeek, Capacity + tous les parkings)
    input_dict = {col: [0] for col in expected_features}
    
    # On met les bonnes valeurs pour les variables de base
    input_dict['Hour'] = [heure]
    input_dict['DayOfWeek'] = [jour_choisi]
    input_dict['Capacity'] = [capacite]
    
    # On met le chiffre "1" uniquement dans la colonne du parking sélectionné (One-Hot Encoding)
    nom_colonne_parking = "SystemCodeNumber_" + parking_choisi
    if nom_colonne_parking in input_dict:
        input_dict[nom_colonne_parking] = [1]
        
    X_input = pd.DataFrame(input_dict)
    
    try:
        # 4. Faire la prédiction
        prediction = model.predict(X_input)
        places_occupees = int(prediction[0])
        
        # Logique pour éviter que l'occupation soit < 0 ou > Capacité
        places_occupees = min(places_occupees, capacite)
        places_occupees = max(places_occupees, 0)
        
        taux_remplissage = (places_occupees / capacite) * 100
        
        # 5. Affichage visuel du résultat
        st.markdown("---")
        st.subheader("📊 Résultat :")
        
        st.metric(label="Nombre de places occupées estimées", value=f"{places_occupees} / {capacite}")
        
        st.progress(taux_remplissage / 100.0)
        
        # Couleurs et messages en fonction du remplissage
        if taux_remplissage >= 90:
            st.error(f"⚠️ Alerte : Le parking sera très rempli ({taux_remplissage:.1f}%). Difficile de se garer.")
        elif taux_remplissage >= 60:
            st.warning(f"🟠 Attention : Le parking sera moyennement occupé ({taux_remplissage:.1f}%).")
        else:
            st.success(f"🟢 Parfait : Le parking aura beaucoup de places libres ({taux_remplissage:.1f}%).")
            
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de la prédiction.\n\n Détail ({e})")
