import streamlit as st
from settings import TEST_ACCOUNT, PREAUTHORIZED
from streamlit_authenticator import Authenticate


def auth():
    authenticator = Authenticate(
        TEST_ACCOUNT,
        'cookie_name',
        'signature_key',
        preauthorized=PREAUTHORIZED
    )
    name, authentication_status, username = authenticator.login("Login", "main")
    if authentication_status:
        authenticator.logout("Logout", "main")
    elif authentication_status is False:
        st.error("Username or Password is incorrect")
    elif authentication_status is None:
        st.warning("Please input Username and Password")

    return authenticator, name, authentication_status, username
