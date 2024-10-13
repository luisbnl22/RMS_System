#streamlit run rms_app.py

import streamlit as st
import requests
from datetime import time
import pandas as pd
import streamlit as st
import requests
from datetime import time
import pandas as pd

# Set page configuration
st.set_page_config(page_title="RMS", layout="wide")

# Initialize session state for managing selected option and login role
if 'login_role' not in st.session_state:
    st.session_state.login_role = None
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None

# CSS to style labels as subtle clickable elements
st.markdown(
    """
    <style>
    .clickable-label {
        font-size: 20px;
        cursor: pointer;
        color: #3498db;
        margin: 10px 0;
    }
    .clickable-label:hover {
        color: #2980b9;
    }
    .centered-title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        margin-top: -50px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display RMS in the center of the page
st.markdown('<div class="centered-title">RMS</div>', unsafe_allow_html=True)

# Check if user is logged in; if not, show login page
if st.session_state.login_role is None:
    st.subheader("Please select your role to login:")
    
    if st.button("Client"):
        st.session_state.login_role = "Client"
    if st.button("Admin"):
        st.session_state.login_role = "Admin"

# If logged in, show content based on role
if st.session_state.login_role == "Client":
    st.sidebar.title("Client Menu")
    if st.sidebar.button("Add Order"):
        st.session_state.selected_option = "Add Order"
    if st.sidebar.button("View Status"):
        st.session_state.selected_option = "View Status"
    if st.sidebar.button("testenew"):
        st.session_state.selected_option = "testenew"
    
    # Logic for each client option
    if st.session_state.selected_option == "Add Order":
        st.subheader("Add a New Order")

        # Simulate a dropdown with plates from a menu
        menu_items = ["Spaghetti", "Burger", "Salad", "Pizza", "Sushi"]
        selected_plate = st.selectbox("Select a Plate", options=menu_items)

        # Input fields for name, contact, and available hour
        person_name = st.text_input("Name of Person")
        contact_info = st.text_input("Contact Information")
        available_hour = st.time_input("Suggested Available Hour", time(12, 0))

        # Submit order to FastAPI backend
        if st.button("Submit Order"):
            if person_name and contact_info:
                order_data = {
                    "id": len(requests.get("http://127.0.0.1:8000/orders/").json()) + 1,
                    "name": person_name,
                    "contact": contact_info,
                    "plate": selected_plate,
                    "available_hour": available_hour.strftime('%H:%M')
                }
                response = requests.post("http://127.0.0.1:8000/orders/", json=order_data)
                if response.status_code == 200:
                    st.success("Order submitted successfully!")
                else:
                    st.error("Failed to submit the order.")
            else:
                st.error("Please fill out all the fields.")

    elif st.session_state.selected_option == "View Status":
        st.subheader("View Order Status")

        # Fetch orders from FastAPI
        response = requests.get("http://127.0.0.1:8000/orders/")
        if response.status_code == 200:
            orders = response.json()

            df = pd.DataFrame(orders)
            if orders:
                st.dataframe(df)
            else:
                st.write("No orders found.")
        else:
            st.error("Failed to fetch order statuses.")

elif st.session_state.login_role == "Admin":
    st.sidebar.title("Admin Menu")
    st.subheader("Admin Dashboard")
    # Admin-specific features can be added here
    # For now, you can use some placeholder options or implement additional functionality as needed.

    st.write("Welcome, Admin! More features coming soon.")
