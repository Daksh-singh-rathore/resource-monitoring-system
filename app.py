
import streamlit as st

st.set_page_config(
    page_title="Grevia | Campus Sustainability",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

from database import init_db
from modules.add_usage import show_add_usage
from modules.dashboard import show_dashboard
from modules.graph import show_graphs
from modules.reports import show_reports


# Initialize existing database
init_db()


# -------------------- FRONTEND THEME --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --forest: #103F32;
    --forest-dark: #0B3027;
    --green: #246B50;
    --mint: #DCEACB;
    --lime: #E8F0A9;
    --canvas: #F7F7F0;
    --card: #FFFFFF;
    --text: #253D32;
    --muted: #829087;
    --border: #E9ECE3;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: var(--canvas);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        var(--forest-dark) 0%,
        var(--forest) 100%
    );
    border-right: none;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1rem;
}

[data-testid="stSidebar"] * {
    color: #F4F6E9;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 5px 4px 24px 4px;
}

.brand-icon {
    width: 48px;
    height: 48px;
    border-radius: 15px;
    background: #285C46;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
}

.brand-name {
    font-family: 'Manrope', sans-serif;
    font-size: 25px;
    line-height: 1.2;
    font-weight: 800;
    color: #FFFFFF;
}

.brand-subtitle {
    font-size: 11px;
    margin-top: 4px;
    color: #C0D4C5;
    letter-spacing: .3px;
}

.sidebar-label {
    color: #B4CDBA;
    font-size: 10px;
    letter-spacing: 2px;
    font-weight: 700;
    margin: 4px 0 12px 8px;
}

/* Navigation */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 8px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: transparent;
    padding: 12px 13px;
    border-radius: 11px;
    border: 1px solid transparent;
    transition: background .2s ease;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,.09);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: rgba(220,234,203,.15);
    border-color: rgba(220,234,203,.18);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    font-weight: 600;
    font-size: 13px;
}

/* Sidebar daily limit control */
[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
    color: #203A2D;
    background: #FFFFFF;
    border-radius: 9px;
}

.sidebar-note {
    background: rgba(255,255,255,.08);
    border: 1px solid rgba(255,255,255,.13);
    border-radius: 13px;
    padding: 14px;
    color: #E2EBDD;
    font-size: 12px;
    line-height: 1.7;
}

.sidebar-note strong {
    color: #E8F0A9;
}

/* Main headings */
h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    color: var(--text);
    letter-spacing: -.7px;
}

h2 {
    font-size: 25px !important;
}

h3 {
    font-size: 18px !important;
}

.eyebrow {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #66816D;
    margin-bottom: 8px;
}

.page-title {
    font-family: 'Manrope', sans-serif;
    font-size: clamp(27px, 3vw, 38px);
    font-weight: 800;
    letter-spacing: -1.5px;
    line-height: 1.2;
    color: #263B30;
    margin-bottom: 10px;
}

.page-subtitle {
    color: #7C897F;
    font-size: 14px;
    margin-bottom: 26px;
}

/* Hero banner */
.hero {
    position: relative;
    overflow: hidden;
    min-height: 285px;
    padding: 34px 35px;
    border-radius: 25px;
    margin: 22px 0 32px 0;
    background:
        radial-gradient(
            circle at 87% 24%,
            #EBCB80 0,
            #EBCB80 44px,
            transparent 46px
        ),
        radial-gradient(
            ellipse at 88% 120%,
            #769F70 0,
            #769F70 18%,
            transparent 18.5%
        ),
        linear-gradient(
            112deg,
            #123E31 0%,
            #24664A 65%,
            #357653 100%
        );
    box-shadow: 0 12px 28px rgba(20,65,46,.12);
}

.hero:after {
    content: "";
    position: absolute;
    width: 290px;
    height: 150px;
    right: -20px;
    bottom: -76px;
    border-radius: 50% 50% 0 0;
    background: rgba(198,221,157,.28);
    transform: rotate(-12deg);
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 650px;
}

.hero-eyebrow {
    color: #D8E6A6;
    font-size: 11px;
    letter-spacing: 1.7px;
    font-weight: 800;
    margin-bottom: 16px;
}

.hero-title {
    color: #FFFFFF;
    font-family: 'Manrope', sans-serif;
    font-size: clamp(27px, 3.4vw, 42px);
    line-height: 1.2;
    letter-spacing: -1.5px;
    font-weight: 800;
}

.hero-title span {
    color: #E8F0A9;
}

.hero-description {
    color: #E0EDE3;
    max-width: 530px;
    font-size: 14px;
    line-height: 1.8;
    margin-top: 14px;
}

.hero-pill {
    display: inline-block;
    margin-top: 20px;
    padding: 10px 14px;
    background: #E8F0A9;
    color: #284A32;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 800;
}

/* Metrics and charts */
[data-testid="stMetric"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 21px 20px;
    box-shadow: 0 5px 16px rgba(32,65,43,.035);
}

[data-testid="stMetricLabel"] {
    color: #78887D;
    font-size: 13px;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: var(--forest);
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
}

[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 8px;
}

[data-testid="stDataFrame"],
[data-testid="stTable"] {
    border: 1px solid var(--border);
    border-radius: 13px;
    overflow: hidden;
}

/* Forms and input fields */
[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 22px;
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {
    border-radius: 10px;
    border-color: #DDE5D9;
}

label, [data-testid="stWidgetLabel"] p {
    color: #405D4B;
    font-weight: 600;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background: var(--forest);
    color: #FFFFFF;
    border: 1px solid var(--forest);
    border-radius: 11px;
    min-height: 42px;
    padding: 8px 17px;
    font-weight: 700;
    transition: all .2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #285F45;
    border-color: #285F45;
    color: #FFFFFF;
    transform: translateY(-1px);
}

.stDownloadButton > button {
    background: #E8F0A9;
    color: #284A32;
    border: 1px solid #DCE69C;
    border-radius: 11px;
    min-height: 42px;
    font-weight: 700;
}

.stDownloadButton > button:hover {
    background: #DCE99A;
    color: #203E2B;
    border-color: #DCE99A;
}

[data-testid="stAlert"] {
    border-radius: 13px;
}

hr {
    border-color: #E4E9DE;
}

.footer {
    color: #849187;
    text-align: center;
    font-size: 11px;
    padding: 25px 0 5px 0;
}

@media (max-width: 700px) {
    .hero {
        padding: 25px 21px;
        min-height: 250px;
        border-radius: 19px;
    }

    .hero-title {
        font-size: 29px;
    }

    [data-testid="stMetric"] {
        padding: 14px;
    }
}
</style>
""", unsafe_allow_html=True)


# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🌿</div>
        <div>
            <div class="brand-name">Grevia</div>
            <div class="brand-subtitle">Campus Sustainability</div>
        </div>
    </div>
    <div class="sidebar-label">WORKSPACE</div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Add Resource Usage",
            "Graphs & Insights",
            "Reports",
        ],
        format_func=lambda item: {
            "Dashboard": "▦   Dashboard",
            "Add Resource Usage": "＋   Log resource use",
            "Graphs & Insights": "◷   Graphs & insights",
            "Reports": "↓   Reports & exports",
        }[item],
        label_visibility="collapsed",
    )

    st.divider()

    daily_limit = st.number_input(
        "Daily water limit (litres)",
        min_value=1.0,
        value=500.0,
        step=50.0,
    )

    st.markdown("""
    <div class="sidebar-note">
        <strong>🌱 Grevia Earth Watch</strong><br>
        Better data. Greener decisions.<br>
        Track campus resources and identify opportunities to reduce wastage.
    </div>
    """, unsafe_allow_html=True)


# -------------------- PAGE CONTENT --------------------
page_info = {
    "Dashboard": {
        "eyebrow": "GREEN CAMPUS",
        "title": "Let's Make Our Campus Greener",
        "subtitle": "A simple view of your campus resource footprint.",
        "hero1": "Better data.",
        "hero2": "Greener decisions.",
        "description": (
            "Monitor daily resource use, spot unusual consumption, "
            "and turn awareness into action."
        ),
        "tag": "＋  Add an entry",
    },
    "Add Resource Usage": {
        "eyebrow": "RESOURCE TRACKING",
        "title": "Every Resource Counts",
        "subtitle": "Record consumption and help build a more sustainable campus.",
        "hero1": "Track today.",
        "hero2": "Improve tomorrow.",
        "description": (
            "Log water, electricity and materials in one place "
            "to keep your resource records organized."
        ),
        "tag": "＋  Record resource use",
    },
    "Graphs & Insights": {
        "eyebrow": "CAMPUS ANALYTICS",
        "title": "Turn Resource Data Into Action",
        "subtitle": "Explore trends and discover where resources are being used.",
        "hero1": "See the patterns.",
        "hero2": "Make smarter choices.",
        "description": (
            "Compare classrooms, understand consumption trends, "
            "and keep an eye on usage limits."
        ),
        "tag": "↗  Explore insights",
    },
    "Reports": {
        "eyebrow": "REPORTS & EXPORTS",
        "title": "Your Campus, Clearly Reported",
        "subtitle": "Review resource records and export data when you need it.",
        "hero1": "Measure progress.",
        "hero2": "Share the impact.",
        "description": (
            "Access your recorded resource usage and download "
            "reports for further analysis."
        ),
        "tag": "↓  View reports",
    },
}

info = page_info[page]

st.markdown(
    f"""
    <div class="eyebrow">{info["eyebrow"]}</div>
    <div class="page-title">{info["title"]}</div>
    <div class="page-subtitle">{info["subtitle"]}</div>

    <div class="hero">
        <div class="hero-content">
            <div class="hero-eyebrow">BETTER DATA. GREENER DECISIONS.</div>
            <div class="hero-title">
                {info["hero1"]}<br>
                <span>{info["hero2"]}</span>
            </div>
            <div class="hero-description">
                {info["description"]}
            </div>
            <div class="hero-pill">{info["tag"]}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# -------------------- EXISTING APP FUNCTIONALITY --------------------
if page == "Dashboard":
    st.markdown(
        '<div class="eyebrow">AT A GLANCE</div>',
        unsafe_allow_html=True,
    )
    st.subheader("Greener Perspective")
    show_dashboard(daily_limit)

elif page == "Add Resource Usage":
    show_add_usage()

elif page == "Graphs & Insights":
    show_graphs(daily_limit)

elif page == "Reports":
    show_reports()


# -------------------- FOOTER --------------------
st.markdown("""
<div class="footer">
    GREVIA · CAMPUS SUSTAINABILITY · BETTER DATA, GREENER DECISIONS
</div>
""", unsafe_allow_html=True)
