import streamlit as st
import pickle
import time

#chargement du module
with open('regS.pkl', 'rb') as file:
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

# Encodage de la région
region_mapping = {'southwest': 0, 'southeast': 1, 'northwest': 2, 'northeast': 3}
region_encoded = region_mapping[region]

# Préparation des données (6 features attendues par le modèle)
input_data = [[age, sex_encoded, bmi, children, smoker_encoded, region_encoded]]

# Prédiction
if st.button('🔮 Prédire les charges médicales', type='primary', use_container_width=True):
    with st.spinner('Calcul en cours...'):
        prediction = model.predict(input_data)[0]
        time.sleep(1)

    st.success("✅ Prédiction terminée avec succès!")
    st.balloons()

    # Affichage du montant en grand avec mise en forme
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin: 20px 0;">
            <h1 style="color: white; font-size: 3.5em; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                💰 ${round(prediction):,}
            </h1>
            <p style="color: white; font-size: 1.3em; margin-top: 10px; opacity: 0.9;">
                Charges médicales annuelles estimées
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    # Informations supplémentaires
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("👤 Âge", f"{age} ans")
        st.metric("🚬 Fumeur", smoker)
    with col_info2:
        st.metric("⚖️ IMC", f"{bmi}")
        st.metric("📍 Région", region)
    with col_info3:
        st.metric("👥 Enfants", children)
        st.metric("⚧️ Sexe", sex)