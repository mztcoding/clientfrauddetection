
# Libraries
import joblib
import numpy as np
import streamlit as st
from data import *  # Data
from graphs import *  # Graph Functions
import base64
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from streamlit_option_menu import option_menu

# Defining Functions

def nextpage():
    if username == "admin" and password == "123":
        st.session_state.page += 1
    else:
        st.error("Incorrect username or password")

def restart():
    st.session_state.page = 0

# Make predictions function
def predict(data, amt):
    encoded_values = encoder.transform([data])
    encoded_data = np.insert(encoded_values, 0, amt)
    print(encoded_data)
    prediction = model.predict([encoded_data])
    return prediction


# def display_graph(graph_type):
#     if graph_type == 'fraud transaction':
#         d = df["is_fraud"].value_counts().reset_index()
#         d.columns = ['is_fraud', 'count']
#         fig = px.pie(d, values="count", names=['No', 'Yes'], hole=0.40, opacity=0.9,
#         labels={"is_fraud": "Fraud", "count": "Number of Samples"})
#         fig.update_layout(title=dict(text="Pie Chart of Fraudulent Transactions"))
#         fig.update_traces(textposition="outside", textinfo="percent+label")
#         st.plotly_chart(fig)  # Display the Plotly figure in Streamlit

# def display_graph(graph_type):
#     if graph_type == 'fraud transaction':
#         d = df["is_fraud"].value_counts().reset_index()
#         d.columns = ['is_fraud', 'count']

#         # Create the pie chart with Plotly
#         fig = px.pie(d, values="count", names=['No', 'Yes'], hole=0.40, opacity=0.9,
#                      labels={"is_fraud": "Fraud", "count": "Number of Samples"})

#         # Update layout to adjust the title style and add margin to move the graph down
#         fig.update_layout(
#             title=dict(
#                 text="Pie Chart of Fraudulent Transactions",
#                 font=dict(size=22, color="black", family="Arial", weight="normal"),  # Normal weight (not bold)
#                 x=0.5,  # Center the title horizontally
#                 xanchor='center',
#                 yanchor='top'
#             ),
#             margin=dict(t=80)  # Add margin at the top to move the graph down (60px from the top)
#         )
        
#         # Update trace properties
#         fig.update_traces(textposition="outside", textinfo="percent+label")
        
#         # Display the Plotly figure in Streamlit
#         st.plotly_chart(fig)


def display_graph(graph_type):
    if graph_type == 'fraud transaction':
        d = df["is_fraud"].value_counts().reset_index()
        d.columns = ['is_fraud', 'count']

        # Create the pie chart with Plotly
        fig = px.pie(d, values="count", names=['No', 'Yes'], hole=0.40, opacity=0.9,
                     labels={"is_fraud": "Fraud", "count": "Number of Samples"})

        # Update layout to adjust the title style and move the pie chart down
        fig.update_layout(
            title=dict(
                text="Pie Chart of Fraudulent Transactions",
                font=dict(size=22, color="black", family="Arial", weight="normal"),  # Normal weight (not bold)
                x=0.5,  # Center the title horizontally
                xanchor='center',
                yanchor='top'
            ),
            margin=dict(t=100, b=40),  # Adds a top margin to the entire chart, b=40 for space at the bottom
            title_y=0.95  # Keep the title in place near the top
        )
        
        # Update trace properties
        fig.update_traces(textposition="outside", textinfo="percent+label")
        
        # Display the Plotly figure in Streamlit
        st.plotly_chart(fig)




    elif graph_type == 'gender analysis': 
        df_fraud = df[df['is_fraud'] == 1]
        plt.figure(figsize=(5, 2))  # Shorten the height of the plot
        sns.set()
        plt.title('Gender Analysis of Fraud Persons', fontsize=10)
        sns.countplot(x=df_fraud['gender'], color='tomato', width=0.3)  # Set bar width to 0.5 (default is 0.8)
        plt.xlabel('Gender')
        plt.ylabel('Count')
        st.pyplot(plt)  # Display the seaborn figure in Streamlit

        
    elif graph_type == 'category analysis':
        df_fraud = df[df['is_fraud'] == 1]
        plt.figure(figsize=(10, 5))  # Adjust figure size to be shorter
        sns.set()
        plt.suptitle('Category Analysis of Fraud Persons')
        sns.countplot(x='category', data=df_fraud, palette='winter')
        plt.xlabel('Transaction Category')
        plt.ylabel('Number of Transactions')
        plt.xticks(rotation=45)
        st.pyplot(plt)  # Display the seaborn figure in Streamlit


    elif graph_type == 'amount distribution':
        df_fraud = df[df['is_fraud'] == 1]
        amounts = df_fraud['amt']
        bins = [0, 100, 500, 1000, 5000]
        labels = ['0-100', '101-500', '501-1000', '1001-5000']
        df_fraud['amount_range'] = pd.cut(amounts, bins=bins, labels=labels)
        plt.figure(figsize=(8, 4))  # Shorten the height of the plot
        sns.set(style="whitegrid")
        sns.countplot(x='amount_range', data=df_fraud, palette='summer')
        plt.title('Amount Distribution Across Different Ranges')
        plt.xlabel('Amount Range')
        plt.ylabel('Frequency')
        st.pyplot(plt)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = 0

# Load models (only once)
model = joblib.load('model.pkl')
encoder = joblib.load('encoder_model.pkl')



if st.session_state.page == 0:
    # Inject CSS for the login page
    st.markdown(
        '''
        <style>
            /* Style for the text input field */
            div[data-baseweb="input"] {
                # margin: auto;
                max-width: 400px;
                border: 2px solid #007bff; /* Blue border */
                border-radius: 8px; /* Rounded corners */
            }
            div[data-baseweb="input"] > div {
                padding: 10px 0 10px 10px; /* Padding inside the input */
                background-color: transparent;
            }
            div[data-testid="stVerticalBlockBorderWrapper"] {
                display: flex;
                margin: 50px auto 0;
                width: 460px;
                border: 2px solid #007bff; /* Blue border */
                padding: 30px;
                border-radius: 8px; /* Rounded corners */
                # background-color: #ffbb00;
            }

            /* Styling for submit button */
            button {
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* Soft shadow for button */
                border-radius: 4px; /* Rounded button corners */
                padding: 10px; /* Padding for the button */
                # display: none;
            }
        </style>
        ''',
        unsafe_allow_html=True
    )

    # Wrapping the header and form inputs inside the box
    # st.header(':blue[Login]')  # Centered login header
    st.markdown('<div class="custom-div">', unsafe_allow_html=True)
    st.markdown('<h1>Login</h1>', unsafe_allow_html=True)
    username = st.text_input("**Username:**")  # Username input
    password = st.text_input("**Password:**", type="password")  # Password input
    st.button("**Submit**", on_click=nextpage)  # Submit button
    st.markdown('</div>', unsafe_allow_html=True)

    # with st.form("login_form"):
    #     username = st.text_input("Username")
    #     password = st.text_input("Password", type="password")
        
    #     # Submit button
    #     # st.button("**Submit**", on_click=nextpage)
    #     st.form_submit_button("Submit",on_click=nextpage)


elif st.session_state.page == 1:
    page_bg_img = f'''
    <style>
            /* Minimalist Sidebar styling */
            [data-testid=stSidebar] {{
                background-color: white;
                padding: 20px;
                border: 2px solid black;
                margin-top: -100px;
            }}
            /* Sidebar link styling */
            .sidebar-link {{
                display: block;
                padding: 10px 0;
                font-size: 18px;
                color: #333;
                text-decoration: none;
            }}
            .sidebar-link:hover {{
                color: #ff0000;
            }}
            /* Add margin to move the images down by 50px */
            .image-container img {{
                margin-top: 50px;
            }}
    </style>
    '''

    # Inject custom CSS
    st.markdown(page_bg_img, unsafe_allow_html=True)

    with st.sidebar:
        # Custom CSS to adjust the logo position
        st.markdown(
            '''
            <style>
                /* Move the logo upwards by 100px */
                img {{
                    margin-top: -100px;  
                }}
            </style>
            ''',
            unsafe_allow_html=True
        )
        # Increase logo width
        st.image("./logo.jpg", width=200, use_column_width=False, output_format="auto", caption="")  # Increase logo width
        
        # Sidebar with menu options
        selected = option_menu("Main Menu", ["Home", 'Analytics', 'About', 'Contact Us'],
                               icons=['house', 'file-earmark-check', 'cloud-arrow-down', 'info-square', 'envelope'],
                               menu_icon="cast", default_index=0,
                               styles={"nav-link-selected": {"background-color": "green"}})

    if selected == "Home":
        st.header(':blue[Transaction Fraud Prediction]')

        # Streamlit page content
        amt = st.number_input('**:green[Amount of Transaction in K]**')

        cat = st.selectbox("**:green[Category]**", categories)

        gen = st.selectbox("**:green[Gender]**", genders)

        city = st.selectbox("**:green[City]**", cities)

        state_name = st.selectbox("**:green[State]**", list(states_dict.values()))
        state = [abbr for abbr, name in states_dict.items() if name == state_name][0]

        job = st.selectbox("**:green[Job]**", jobs)

        sub = st.button('**Check Transaction**')

        data = [cat, gen, city, state, job]

        # Prediction function
        if sub:
            predictions = predict(data, amt)
            if predictions[0] == 0:
                st.success('This Transaction is Safe.', icon="✅")
            else:
                st.error('This Transaction may be Fraudulent.', icon="⚠️")

    elif selected == "Analytics":
        st.header('Analytics', divider='rainbow')
        # Sample dataset (you can replace this with actual data)

        data = pd.DataFrame({
            'Category': ['A', 'B', 'C', 'D'],
            'Values': [4, 3, 2, 1]
        })

        # Display an option menu above the graph
        selected_graph = option_menu(
            menu_title=None,
            options=['fraud transaction', 'gender analysis', 'category analysis', 'amount distribution'],
            icons=['housscse', 'filecsc-earmark-check', 'cloudcsc-arrow-down', 'infocscs-square', 'envelopecsc'],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {
                    "padding": "0px",
                    "background-color": "#f0f0f0", 
                    "margin-bottom": "20px"  # Set margin-bottom to 20px for more space below nav
                },
                "nav-link": {
                    "font-size": "16px", 
                    "color": "black",
                    "min-width": "fit-content",
                    "text-align": "center", 
                    "font-weight": "normal"  # Ensure text is normal weight
                },
                "nav-link-selected": {
                    "background-color": "#4a90e2", 
                    "color": "white", 
                    "font-weight": "normal"  # Prevent bold on selection
                },
            }
        )

        # Display the selected graph
        display_graph(selected_graph)

    elif selected == "About":
        st.header('About', divider='rainbow')
        st.write(':blue[**Draikin is a prediagnostic progressive web app that helps to scan and analyse skin pathology.**]')

    elif selected == "Contact Us":
        st.header('Contact Us', divider='rainbow')
        st.write(':blue[If you have any questions about this Progressive Web App. You can contact us:]')
        st.write(':green[**By email: motubas@gmail.com**]')
