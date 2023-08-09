import streamlit as st
from settings import TEST_ACCOUNT, PREAUTHORIZED, HIDE_DEFAULT_FORMAT
from streamlit_authenticator import Authenticate


st.caption(HIDE_DEFAULT_FORMAT, unsafe_allow_html=True)

authenticator = Authenticate(
    TEST_ACCOUNT,
    'cookie_name',
    'signature_key',
    preauthorized={"emails": PREAUTHORIZED}
)

if "authentication_status" in st.session_state:
    if st.session_state["authentication_status"]:
        try:
            if authenticator.reset_password(st.session_state["username"], 'Reset password'):
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)
    else:
        st.info("Please log in first")
