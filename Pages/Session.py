import streamlit as st
from settings import HIDE_DEFAULT_FORMAT

st.caption(HIDE_DEFAULT_FORMAT, unsafe_allow_html=True)
st.json(st.session_state)
