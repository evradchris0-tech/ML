import streamlit as st


st.title('Welcome to BMI Calculator')

weight = st.number_input("enter your weight in kgs")
status = st.radio('Select your heigh format:', ('cms','meters','feet'))


try:
    if status=='cms':
        height = st.number_input('Centimerters')
        bmi = weight/((height/100)**2)

    elif status == 'meters':
        height = st.number_input('meters')
        bmi = weight/((height)**2)
    else:
        height = st.number_input('feet')
        bmi = weight/((height/3.28)**2)
except:
    print('Zero divison error')

if (st.button('Calculate BMI')):
    st.write('Your BMI index is {}'.format(round(bmi)))

    if bmi<16:
        st.error('Your are extremely underweight')
    elif (bmi>=16 and bmi <18.5):
        st.warning('Your are underweight')
    elif (bmi>=18.5 and bmi <25):
        st.success('Your are Healthy')
    elif (bmi>=25 and bmi <30):
        st.warning('Your are overrweight')
    elif bmi>=30:
        st.error('Your are extremely overrweight')
