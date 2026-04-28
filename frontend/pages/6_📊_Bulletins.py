import streamlit as st
from frontend.components.auth import require_auth
from frontend.components.sidebar import render_sidebar
from frontend.api.client import get

st.set_page_config(page_title="Bulletins", page_icon="📊", layout="wide")
require_auth()
render_sidebar()

st.title("📊 Bulletins scolaires")
st.info("Module en cours de développement — les bulletins seront générés ici par trimestre.")

# Placeholder fonctionnel
role = st.session_state.get("role")
user_id = st.session_state.get("user_id")
student_id = st.session_state.get("student_id", user_id)

trimester = st.selectbox("Trimestre", ["Trimestre 1", "Trimestre 2", "Trimestre 3"])
school_year = st.text_input("Année scolaire", value="2025-2026")

if role in ("student", "parent"):
    st.write(f"Bulletin de l'élève #{student_id} — {trimester} {school_year}")
    st.warning("Connectez votre route `/api/bulletins/` pour afficher les données réelles.")
