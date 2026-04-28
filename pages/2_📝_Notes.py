import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import streamlit as st
import pandas as pd
import plotly.express as px
from frontend.components.auth import require_auth
from frontend.components.sidebar import render_sidebar
from frontend.api.client import get, post

st.set_page_config(page_title="Notes", page_icon="📝", layout="wide")
require_auth()
render_sidebar()

st.title("📝 Notes")
role = st.session_state.get("role")
user_id = st.session_state.get("user_id")
student_id = st.session_state.get("student_id", user_id)

# --- Consultation ---
st.subheader("Consulter les notes")
target_id = st.number_input("ID de l'élève", min_value=1, step=1, value=student_id)

if st.button("Charger les notes"):
    grades = get(f"/api/grades/student/{target_id}")
    if grades:
        df = pd.DataFrame(grades)
        df["note_sur_20"] = (df["value"] / df["max_value"] * 20).round(2)
        st.dataframe(
            df[["title", "grade_type", "note_sur_20", "coefficient", "appreciation", "graded_at"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "title": "Évaluation",
                "grade_type": "Type",
                "note_sur_20": st.column_config.NumberColumn("Note /20", format="%.2f"),
                "coefficient": "Coeff.",
                "appreciation": "Appréciation",
                "graded_at": "Date",
            },
        )

        # Graphique évolution
        fig = px.line(
            df.sort_values("graded_at"),
            x="graded_at",
            y="note_sur_20",
            title="Évolution des notes",
            markers=True,
            labels={"graded_at": "Date", "note_sur_20": "Note /20"},
        )
        fig.add_hline(y=10, line_dash="dash", line_color="red", annotation_text="Seuil 10/20")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune note enregistrée.")

# --- Saisie (prof / admin) ---
if role in ("teacher", "admin"):
    st.divider()
    st.subheader("Saisir une note")
    with st.form("grade_form"):
        col1, col2 = st.columns(2)
        with col1:
            s_id = st.number_input("ID élève", min_value=1, step=1)
            sub_id = st.number_input("ID matière", min_value=1, step=1)
            cl_id = st.number_input("ID classe", min_value=1, step=1)
        with col2:
            value = st.number_input("Note", min_value=0.0, max_value=20.0, step=0.5)
            coeff = st.number_input("Coefficient", min_value=0.5, step=0.5, value=1.0)
            grade_type = st.selectbox("Type", ["Interrogation", "Devoir surveillé", "Travaux pratiques", "Oral", "Projet", "Contrôle"])
        title = st.text_input("Intitulé de l'évaluation")
        appreciation = st.text_area("Appréciation (optionnel)")
        graded_at = st.date_input("Date")
        submitted = st.form_submit_button("Enregistrer")

    if submitted and title:
        result = post("/api/grades/", {
            "student_id": s_id,
            "subject_id": sub_id,
            "classe_id": cl_id,
            "value": value,
            "max_value": 20.0,
            "coefficient": coeff,
            "grade_type": grade_type,
            "title": title,
            "appreciation": appreciation or None,
            "graded_at": str(graded_at),
        })
        if result:
            st.success("Note enregistrée ✓")
