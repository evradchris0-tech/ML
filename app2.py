import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import streamlit as st

@st.cache_data
def load_data(dataset):
    df = pd.read_csv(dataset)
    return df

st.sidebar.image('images/diabetes.jpg')

def main():
    st.markdown("<h1 style='text-align: center; color: brown;'>Diabetes Prediction App</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: black;'>Diabetes study in Cameroun</h2>", unsafe_allow_html=True)

    menu = ['Home', 'Analysis', 'Data Visualization', 'Machine Learning']
    choice = st.sidebar.selectbox("Select a page", menu)
    data = load_data('diabetes.csv')
    if choice == 'Home':
        left,middle,right = st.columns((2,3,2))
        with middle:
            st.image('images/telechargement.jpg', width=300)
        st.write("this application is designed to predict whether a person has diabetes or not based on various health parameters. The dataset used in this application is sourced from a study conducted in Cameroon, which includes information about individuals' health metrics and their diabetes status.")
        st.subheader("About Diabetes")
        st.write("In Cameroon, diabetes is a growing health concern, with increasing prevalence rates due to lifestyle changes and urbanization. The country faces challenges in managing diabetes, including limited access to healthcare services and a lack of awareness about the disease. Efforts are being made to improve diabetes care through public health initiatives, education, and better healthcare infrastructure. Early diagnosis and management are crucial to prevent complications associated with diabetes, such as cardiovascular diseases, kidney failure, and vision problems. Addressing diabetes in Cameroon requires a comprehensive approach involving government policies, healthcare providers, and community engagement to promote healthy lifestyles and improve access to medical care.")

    elif choice == 'Analysis':
        st.subheader("Exploratory Data Analysis")
        st.write(data.head())
        if st.checkbox("Summary"):
            st.write(data.describe())
        elif st.checkbox("Correlation"):
            fig1 = plt.figure(figsize=(15,15))
            st.write(sns.heatmap(data.corr(), annot=True))
            st.pyplot(fig1)

    elif choice == 'Data Visualization':
        if st.checkbox('Countplot'):
            fig2 = plt.figure(figsize=(5,5))
            sns.countplot(data=data, x='Age')
            st.pyplot(fig2)
            
        elif st.checkbox('Scatterplot'):
            fig3 = plt.figure(figsize=(10,10))
            sns.scatterplot(data=data, x='Glucose', y='Age', hue='Outcome')
            st.pyplot(fig3)

    elif choice == 'Machine Learning':
        tab1,tab2,tab3 = st.tabs([":clipboard: Data", ":bar_chart: Visualisation", ":mask: :smile: Prediction"])
        upload_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
        if upload_file:
            df = load_data(upload_file)

            with tab1:
                st.subheader("Load Dataset")
                st.write(df)
            with tab2:
                st.subheader("Histogram Glucose")
                fig4 = plt.figure(figsize=(8,8))
                sns.histplot(data=df, x='Glucose')
                st.pyplot(fig4)
            with tab3:
                model=pickle.load(open('model_dump.pkl', 'rb'))
                prediction = model.predict(df)
                st.subheader("Prediction")
                pp = pd.DataFrame(prediction, columns=['Prediction'])
                ndf = pd.concat([df, pp], axis=1)
                ndf.Prediction.replace({0, 'No Diabetes'}, inplace=True)
                ndf.Prediction.replace({1, 'Diabetes'}, inplace=True)
                st.write(ndf)
if __name__ == '__main__':
    main()
