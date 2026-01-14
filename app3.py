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