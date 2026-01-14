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
    st.markdown(
        """
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 10px; margin-bottom: 20px;">
            <h1 style="color: white; margin: 0;">🩺 Diabetes Prediction App</h1>
            <p style="color: white; font-size: 1.2em; margin: 10px 0 0 0; opacity: 0.9;">Diabetes study in Cameroon</p>
        </div>
        """,
        unsafe_allow_html=True
    )

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
                if st.button('🔮 Prédire le diabète', type='primary', use_container_width=True):
                    with st.spinner('Analyse en cours...'):
                        model=pickle.load(open('model_dump.pkl', 'rb'))
                        prediction = model.predict(df)

                    st.success("✅ Prédiction terminée avec succès!")

                    # Créer le DataFrame avec les prédictions
                    pp = pd.DataFrame(prediction, columns=['Prediction'])
                    ndf = pd.concat([df, pp], axis=1)
                    ndf['Status'] = ndf['Prediction'].apply(lambda x: '❌ Diabetes' if x == 1 else '✅ No Diabetes')

                    # Statistiques
                    diabetes_count = (ndf['Prediction'] == 1).sum()
                    no_diabetes_count = (ndf['Prediction'] == 0).sum()
                    total = len(ndf)

                    # Affichage des statistiques
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("📊 Total", total)
                    with col2:
                        st.metric("✅ No Diabetes", f"{no_diabetes_count} ({no_diabetes_count/total*100:.1f}%)")
                    with col3:
                        st.metric("❌ Diabetes", f"{diabetes_count} ({diabetes_count/total*100:.1f}%)",
                                 delta=f"{diabetes_count/total*100:.1f}%", delta_color="inverse")
                    st.markdown("---")

                    # Afficher le tableau des résultats
                    st.subheader("📋 Résultats détaillés")
                    st.dataframe(ndf, use_container_width=True, height=400)
if __name__ == '__main__':
    main()
