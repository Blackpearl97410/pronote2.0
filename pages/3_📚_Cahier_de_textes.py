import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import streamlit as st
import pandas as pd
from datetime import date
from frontend.components.auth import require_auth
from frontend.components.sidebar import render_sidebar
from frontend.api.client import get, post

st.set_page_config(page_title="Cahier de textes", page_icon="📚", layout="wide")
require_auth()
render_sidebar()

st.title("📚 Cahier de textes")
role = st.session_state.get("role")

classe_id = st.number_input("ID de la classe", min_value=1, step=1, value=1)

if st.button("Charger les devoirs"):
    homeworks = get(f"/api/homework/classe/{classe_id}")
    if homeworks:
        df = pd.DataFrame(homeworks)
        df["is_graded"] = df["is_graded"].map({True: "✅ Oui", False: "Non"})
        st.dataframe(
            df[["title", "due_date", "is_graded", "description"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "title": "Devoir",
                "due_date": "À rendre pour",
                "is_graded": "Noté ?",
                "description": "Description",
            },
        )
    else:
        st.info("Aucun devoir enregistré pour cette classe.")

# --- Ajout devoir (prof/admin) ---
if role in ("teacher", "admin"):
    st.divider()
    st.subheader("Ajouter un devoir")
    with st.form("hw_form"):
        title = st.text_input("Intitulé")
        description = st.text_area("Description / contenu du cours")
        col1, col2 = st.columns(2)
        with col1:
            sub_id = st.number_input("ID matière", min_value=1, step=1)
            cl_id = st.number_input("ID classe", min_value=1, step=1)
        with col2:
            due = st.date_input("Date limite", min_value=date.today())
            is_graded = st.checkbox("Devoir noté")
        submitted = st.form_submit_button("Publier")

    if submitted and title:
        result = post("/api/homework/", {
            "subject_id": sub_id,
            "classe_id": cl_id,
            "title": title,
            "description": description or None,
            "due_date": str(due),
            "is_graded": is_graded,
        })
        if result:
            st.success("Devoir publié ✓")
