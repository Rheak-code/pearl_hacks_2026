import streamlit as st

PRIMARY = "#0f0c4b"   # deep navy
SAND    = "#e8d6a8"   # beige
LAV     = "#cac8f6"   # lavender


def apply_theme():
    st.set_page_config(layout="wide")

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Montserrat', sans-serif !important;
        }}

        /* Background */
        .stApp {{
            background-color: {PRIMARY};
        }}

        /* Keep sidebar working */
        section[data-testid="stSidebar"] {{
            background-color: #ffffff;
        }}

        /* Main container spacing */
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1100px;
        }}

        /* Headings */
        h1, h2, h3 {{
            color: white;
        }}

        p, label, span {{
            color: white;
        }}

        /* Card container */
        .mm-card {{
            background: {SAND};
            border-radius: 18px;
            padding: 28px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        }}

        /* Buttons */
        .stButton > button {{
            border-radius: 999px !important;
            padding: 0.8rem 1.4rem !important;
            font-weight: 600 !important;
            border: none !important;
            background: {LAV} !important;
            color: black !important;
        }}

        /* Inputs */
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stSelectbox"] div,
        div[data-testid="stTextArea"] textarea {{
            border-radius: 999px !important;
            padding: 0.75rem 1rem !important;
            background: #f3f3f3 !important;
            color: #111 !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


def topbar():
    st.markdown(
        f"""
        <div style="
            background:{LAV};
            padding:15px 30px;
            margin-bottom:30px;
            border-radius:12px;
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">
            <div style="display:flex;align-items:center;gap:12px;">
                <div style="
                    width:40px;
                    height:40px;
                    border-radius:8px;
                    background:white;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-weight:700;
                    color:{PRIMARY};
                ">
                    M
                </div>
                <div style="
                    font-size:24px;
                    letter-spacing:2px;
                    font-weight:600;
                    color:white;
                ">
                    MOMENTUM
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )