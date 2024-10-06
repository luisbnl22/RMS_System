#streamlit run rms_app.py

import streamlit as st
import requests
from datetime import time
import pandas as pd

# Set page configuration
st.set_page_config(page_title="RMS", layout="wide")

# Initialize session state for managing selected option
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

# Sidebar with clickable labels
with st.sidebar:
    st.title("Menu")
    if st.button("Add Order"):
        st.session_state.selected_option = "Add Order"
    if st.button("View Status"):
        st.session_state.selected_option = "View Status"

# Logic for each option
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
            #for order in orders:
                #st.write(f"Order ID: {order['id']}, Plate: {order['plate']}, Name: {order['name']}, Contact: {order['contact']}, Available Hour: {order['available_hour']}")
            st.dataframe(df)
        else:
            st.write("No orders found.")
    else:
        st.error("Failed to fetch order statuses.")
