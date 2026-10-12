
import streamlit as st


import streamlit as st

st.markdown("""
<style>
/* Main website background */
.stApp {
    background-color: #E8F3DC;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #D5E8C5;
}

/* Containers and form backgrounds */
[data-testid="stForm"] {
    background-color: #F5F9EF;
    border: 1px solid #C5DAB4;
    border-radius: 12px;
    padding: 20px;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #F5F9EF;
    border: 1px solid #C5DAB4;
    padding: 15px;
    border-radius: 12px;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background-color: #729C59;
    color: white;
    border: none;
    border-radius: 8px;
}

/* Button hover */
.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #5B8244;
    color: white;
    border: 1px solid #5B8244;
}
</style>
""", unsafe_allow_html=True)


from database import init_db
from modules.add_usage import show_add_usage
from modules.dashboard import show_dashboard
from modules.graph import show_graphs
from modules.reports import show_reports


st.set_page_config(
    page_title="Resource Wastage Monitoring System",
    page_icon="♻️",
    layout="wide"
)

init_db()

st.sidebar.title("♻️ Resource Monitor")
st.sidebar.caption("Resource Wastage Monitoring System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Resource Usage",
        "Graphs & Insights",
        "Reports"
    ]
)

st.sidebar.divider()

daily_limit = st.sidebar.number_input(
    "Daily water limit (litres)",
    min_value=1.0,
    value=500.0,
    step=50.0
)

if page == "Dashboard":
    show_dashboard(daily_limit)

elif page == "Add Resource Usage":
    show_add_usage()

elif page == "Graphs & Insights":
    show_graphs(daily_limit)

elif page == "Reports":
    show_reports()
