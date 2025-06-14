import streamlit as st
import pandas as pd
import io

from clean_eats import run_clean_eats_flow
from made_active import run_made_active_flow
from elite_meals import run_elite_meals_flow

# --- CONFIG ---
st.set_page_config(page_title="Product Quantity Summary", layout="centered")

# --- CLIENT SELECTOR ---
selected_client = st.radio("Select Client", ["Clean Eats", "Made Active", "Elite Meals"], horizontal=True)

# --- PRODUCT ORDER (shared across clients that use ordering) ---
product_order = [
    "Spaghetti Bolognese",
    "Beef Chow Mein",
    "Shepherd's Pie",
    "Beef Burrito Bowl",
    "Beef Meatballs",
    "Lebanese Beef Stew",
    "Mongolian Beef",
    "Chicken with Vegetables",
    "Chicken with Sweet Potato and Beans",
    "Naked Chicken Parma",
    "Chicken Pesto Pasta",
    "Chicken and Broccoli Pasta",
    "Butter Chicken",
    "Thai Green Chicken Curry",
    "Moroccan Chicken",
    "Steak with Mushroom Sauce",
    "Creamy Chicken & Mushroom Gnocchi",
    "Roasted Lemon Chicken & Potatoes",
    "Beef Lasagna",
    "Bean Nachos with Rice",
    "Lamb Souvlaki",
    "Chicken Fajita Bowl",
    "Steak On Its Own",
    "Chicken On Its Own",
    "Family Mac and 3 Cheese Pasta Bake",
    "Baked Family Lasagna"
]

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Upload Zapiet Production Report CSV or Excel", type=["csv", "xlsx"])
generate = st.button("Generate Report")

if generate and uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(f"File uploaded. Running script for **{selected_client}**...")
        st.subheader("Raw Data Preview")
        st.dataframe(df.head(), use_container_width=True)

        if "Product name" not in df.columns or "Quantity" not in df.columns:
            st.error("File must contain 'Product name' and 'Quantity' columns.")
        else:
            if selected_client == "Clean Eats":
                run_clean_eats_flow(df, product_order)
            elif selected_client == "Made Active":
                run_made_active_flow(df, product_order)
            elif selected_client == "Elite Meals":
                run_elite_meals_flow(df)

    except Exception as e:
        st.error(f"Error processing file: {e}")
