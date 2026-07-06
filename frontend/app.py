import streamlit as st

st.set_page_config(
    page_title="Snap2Cook AI",
    page_icon="🍳",
    layout="wide"
)

st.title("Snap2Cook AI 🍳")
st.markdown("""
Welcome to Snap2Cook AI! 
This multi-agent application will help you reverse-engineer a recipe from a photo of a dish, 
and optionally adapt that recipe based on what you have in your pantry.

### How to use:
1. Go to **Upload Dish** from the sidebar to start by identifying a dish.
2. Go to **My Pantry** to adapt a recipe to your available ingredients.
""")
