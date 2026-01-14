import streamlit as st
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
    children = st.selectbox('Nombre d enfants ?', options=[0, 1, 2, 3, 4, 5], index=0)
    
col5,col6 =st.columns(2)
with col5:
    smoker = st.selectbox('Fumeur ?', ['yes', 'no'])
with col6:
    region = st.selectbox('Region', ['southwest', 'southeast','northwest','northeast'])

# Encodage des variables
sex_encoded = 1 if sex == 'male' else 0
smoker_encoded = 1 if smoker == 'yes' else 0

# Encodage et fréquence de la région
region_mapping = {'southwest': 0, 'southeast': 1, 'northwest': 2, 'northeast': 3}
region_freq_mapping = {'southwest': 0.24308153, 'southeast': 0.27225131, 'northwest': 0.24233358, 'northeast': 0.27225131}

region_encoded = region_mapping[region]
region_freq = region_freq_mapping[region]

# Préparation des données (7 features attendues par le modèle)
input_data = [[age, sex_encoded, bmi, children, smoker_encoded, region_encoded, region_freq]]

# Prédiction
if st.button('Prédire les charges médicales'):
    with st.spinner('Calcul en cours...'):
        prediction = model.predict(input_data)[0]
        time.sleep(1)

    st.success("Prédiction terminée!")
    st.markdown(f"### Charges médicales estimées : **${round(prediction):,}**")
    st.balloons()

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
    
    
