import streamlit as st
from frontend.components.auth import logout


def render_sidebar():
    with st.sidebar:
        st.markdown(f"### 👋 {st.session_state.get('full_name', '')}")
        role_labels = {
            "admin": "🏫 Administration",
            "teacher": "👨‍🏫 Enseignant",
            "student": "👨‍🎓 Élève",
            "parent": "👨‍👩‍👧 Parent",
        }
        role = st.session_state.get("role", "")
        st.caption(role_labels.get(role, role))
        st.divider()

        st.page_link("streamlit_app.py", label="🏠 Accueil")
        st.page_link("pages/1_📅_Emploi_du_temps.py", label="📅 Emploi du temps")
        st.page_link("pages/2_📝_Notes.py", label="📝 Notes")
        st.page_link("pages/3_📚_Cahier_de_textes.py", label="📚 Cahier de textes")
        st.page_link("pages/4_📩_Messagerie.py", label="📩 Messagerie")
        st.page_link("pages/5_🚨_Absences.py", label="🚨 Absences")
        st.page_link("pages/6_📊_Bulletins.py", label="📊 Bulletins")

        st.divider()
        if st.button("🚪 Déconnexion", use_container_width=True):
            logout()
