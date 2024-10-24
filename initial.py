# Libraries
import joblib
import numpy as np
import streamlit as st
from data import *      # Data
from graphs import *  # Graph Functions


# Defining Functions

def nextpage():
    if username == "admin" and password == "123":
        st.session_state.page += 1
    else:
        st.error("Incorrect username or password")

def restart(): st.session_state.page = 0

# Make predictions function
def predict(data, amt):
    encoded_values = encoder.transform([data])
    encoded_data = np.insert(encoded_values, 0, amt)
    print(encoded_data)
    prediction = model.predict([encoded_data])
    return prediction


if "page" not in st.session_state:
    st.session_state.page = 0

if st.session_state.page == 0:
    # Replace the placeholder with some text:
    st.header(':blue[Login]')
    username = st.text_input("**Username:**")
    password = st.text_input("**Password:**", type="password")
    st.button("**Submit**", on_click=nextpage)


elif st.session_state.page == 1:

    model = joblib.load('model.pkl')
    encoder = joblib.load('encoder_model.pkl')

    # Streamlit page
    st.header(':blue[Transaction Fraud Prediction]')

    amt = st.number_input('**:green[Amount of Transaction in K]**')

    cat = st.selectbox("**:green[Category]**", categories)

    gen = st.selectbox("**:green[Category]**", genders)

    city = st.selectbox("**:green[City]**", cities)

    state_name = st.selectbox("**:green[State]**", list(states_dict.values()))
    state = [abbr for abbr, name in states_dict.items() if name == state_name][0]

    job = st.selectbox("**:green[Job]**", jobs)

    sub = st.button('**Check Transaction**')

    data = [cat, gen, city, state, job]

    # prediction function
    if sub:
        predictions = predict(data, amt)
        if predictions[0] == 0:
            st.success('This Transaction is Safe.', icon="✅")
        else:
            st.error('This Trasaction may be Fraudlent.', icon="⚠️")
