import streamlit as st

PRIMARY = "#0f0c4b"   # deep navy
SAND    = "#e8d6a8"   # beige
LAV     = "#cac8f6"   # lavender

def apply_theme():
    st.markdown(
        f"""
        <style>
        /* Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Montserrat', sans-serif !important;
        }}

        /* App background */
        .stApp {{
            background: {PRIMARY};
        }}

        /* Optional: remove Streamlit header + footer */
        header {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}

        /* Make main area wider/centered like a landing page */
        .block-container {{
            padding-top: 2.5rem;
            padding-bottom: 3rem;
            max-width: 1100px;
        }}

        /* Headings */
        h1, h2, h3, p, label, span {{
            color: white;
        }}

        /* Card container (beige sections like your designs) */
        .mm-card {{
            background: {SAND};
            border-radius: 18px;
            padding: 28px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        }}

        /* Accent strip / header bar */
        .mm-topbar {{
            background: {LAV};
            border-radius: 0px;
            padding: 14px 18px;
            margin: -2.5rem -9999px 2rem -9999px; /* full-bleed */
            padding-left: 9999px;
            padding-right: 9999px;
            border-bottom: 3px solid rgba(0,0,0,0.12);
        }}
        .mm-brand {{
            display:flex;
            align-items:center;
            gap:14px;
        }}
        .mm-brand-title {{
            font-size: 34px;
            letter-spacing: 2px;
            color: white;
            font-weight: 500;
        }}
        .mm-nav {{
            float:right;
            display:flex;
            gap:22px;
            align-items:center;
            font-weight:600;
            color: #111;
        }}
        .mm-nav a {{
            text-decoration:none;
            color:#111;
        }}

        /* Buttons: round + on-brand */
        .stButton > button {{
            border-radius: 999px !important;
            padding: 0.9rem 1.3rem !important;
            font-weight: 600 !important;
            border: 0 !important;
            background: {PRIMARY} !important;
            color: white !important;
        }}
        .stButton > button:hover {{
            filter: brightness(1.05);
        }}

        /* Inputs: pill style like your login + personal data page */
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stSelectbox"] div,
        div[data-testid="stTextArea"] textarea {{
            border-radius: 999px !important;
            padding: 0.85rem 1rem !important;
            border: 1px solid rgba(0,0,0,0.15) !important;
            background: #f3f3f3 !important;
            color: #111 !important;
        }}

        /* Make labels dark when inside beige card */
        .mm-card label, .mm-card p, .mm-card span, .mm-card h1, .mm-card h2, .mm-card h3 {{
            color: #123;
        }}

        /* Hide sidebar if you want a pure “website” feel */
        section[data-testid="stSidebar"] {{
            display: none;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )

def topbar():
    st.markdown(
        f"""
        <div class="mm-topbar">
          <div class="mm-brand">
            <div style="width:44px;height:44px;border-radius:8px;background:white;display:flex;align-items:center;justify-content:center;font-weight:700;color:{PRIMARY};">
              M
            </div>
            <div class="mm-brand-title">MOMENTUM</div>
            <div class="mm-nav">
              <a href="#">Login</a>
              <a href="#">About</a>
              <a href="#">Contact Us</a>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )