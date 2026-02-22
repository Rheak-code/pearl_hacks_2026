import streamlit as st
from lib.theme import apply_theme, topbar

apply_theme()
topbar()

st.markdown("<br>", unsafe_allow_html=True)

# Hero area (image + tagline) like your mock
st.markdown(
    """
    <div style="text-align:center;">
      <h1 style="font-weight:500; color:white;">Balance your Money. Own your Future.</h1>
      <div style="width:340px;height:3px;background:#ffffff55;margin:14px auto 22px auto;"></div>
      <p style="max-width:900px;margin:0 auto;color:#ffffffcc;font-size:18px;line-height:1.6;">
        Money is more complex than ever. Rates change, inflation rises, and markets shift—yet most people don’t see how it impacts their everyday finances.
      </p>
      <p style="max-width:900px;margin:18px auto 0 auto;color:#ffffffcc;font-size:18px;line-height:1.6;">
        Momentum gives you a clear view of your financial life — helping you stay balanced as rates, markets, and inflation change.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Login", use_container_width=True):
        st.switch_page("pages/02_Login.py")