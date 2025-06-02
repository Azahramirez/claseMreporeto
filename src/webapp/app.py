import streamlit as st 
from utils.functions import load_data
import plotly.express as px 
import plotly.graph_objects as go


st.set_page_config(
        page_title="BookML Dashboard",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded")
    


def main():
    # Set the title of the dashboard
    st.title("📚 BookML Main Menu 🤖")






if __name__ == "__main__":
    main()