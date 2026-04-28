"""Gestion de la session et de la page de login."""
import streamlit as st
from frontend.api.mock import demo_login
from frontend.api.client import login


def is_logged_in() -> bool:
    return bool(st.session_state.get("token"))


def show_login_page():
    st.title("🎓 Pronote 2.0")
    st.subheader("Connexion")
    st.caption("Astuce: utilise `demo@pronote.local` / `demo` ou le bouton demo pour naviguer sans backend.")

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="votre@email.fr")
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter", use_container_width=True)

    if submitted and email and password:
        result = login(email, password)
        if result:
            st.session_state["token"] = result["access_token"]
            st.session_state["role"] = result["role"]
            st.session_state["full_name"] = result["full_name"]
            st.session_state["user_id"] = result["user_id"]
            st.session_state["student_id"] = result.get("student_id", result["user_id"])
            st.rerun()

    if st.button("Entrer en mode demo", use_container_width=True):
        result = demo_login()
        st.session_state["demo_mode"] = True
        st.session_state["token"] = result["access_token"]
        st.session_state["role"] = result["role"]
        st.session_state["full_name"] = result["full_name"]
        st.session_state["user_id"] = result["user_id"]
        st.session_state["student_id"] = result.get("student_id", result["user_id"])
        st.rerun()


def logout():
    for key in ["token", "role", "full_name", "user_id", "student_id", "demo_mode"]:
        st.session_state.pop(key, None)
    st.rerun()


def require_auth():
    """Appeler en tête de chaque page protégée."""
    if not is_logged_in():
        show_login_page()
        st.stop()
