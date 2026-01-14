import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import time

#chargement du module
with open('reg.pkl', 'rb') as file:
    model = pickle.load(file)
    
st.title('Predicteur de charges d assurances medicales')
#ajout d'une animation
with st.spinner('chargement du modele...'):
    time.sleep(1)
    
#entree  des inputs
col1,col2 = st.columns(2)
with col1:
    age = st.slider('age', 10,100,24)
with col2:
    sex = st.selectbox('sexe', ['male', 'female', 'other'])

col3,col4 =st.columns(2)
with col3:
    bmi = st.number_input('BMI (Indice Masse Corporelle)', 10,50,25)
with col4:
    children = st.selectbox('Nombre d enfants ?', 0,5,1)
    
col5,col6 =st.columns(2)
with col5:
    smoker = st.selectbox('Fumeur ?', ['yes', 'no'])
with col6:
    region = st.selectbox('Region', ['southwest', 'southeast','northwest','northeast'])

# Bouton de prédiction
if st.button('Prédire les charges médicales'):
    # Encodage des variables catégorielles
    sex_encoded = 1 if sex == 'male' else 0
    smoker_encoded = 1 if smoker == 'yes' else 0

    # Encodage de la région
    region_mapping = {
        'southwest': 0,
        'southeast': 1,
        'northwest': 2,
        'northeast': 3
    }
    region_encoded = region_mapping[region]

    # Fréquence de région (valeurs approximatives basées sur le dataset)
    region_freq_mapping = {
        'southwest': 0.243,
        'southeast': 0.272,
        'northwest': 0.242,
        'northeast': 0.243
    }
    region_freq = region_freq_mapping[region]

    # Création du DataFrame pour la prédiction avec valeurs encodées
    input_data = pd.DataFrame({
        'age': [age],
        'sex': [sex_encoded],
        'bmi': [bmi],
        'children': [children],
        'smoker': [smoker_encoded],
        'region': [region_encoded],
        'region frequence encode': [region_freq]
    })

    # Prédiction
    prediction = model.predict(input_data)

    # Affichage du résultat
    st.success(f'💰 Charges médicales estimées : ${prediction[0][0]:,.2f}')

    # Informations supplémentaires
    st.info(f"""
    **Détails de la prédiction:**
    - Âge: {age} ans
    - Sexe: {sex}
    - IMC: {bmi}
    - Nombre d'enfants: {children}
    - Fumeur: {smoker}
    - Région: {region}
    """)