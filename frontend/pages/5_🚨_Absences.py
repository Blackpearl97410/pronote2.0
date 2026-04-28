import streamlit as st
import pandas as pd
from datetime import date, datetime, time
from frontend.components.auth import require_auth
from frontend.components.sidebar import render_sidebar
from frontend.api.client import get, post, patch

st.set_page_config(page_title="Absences", page_icon="🚨", layout="wide")
require_auth()
render_sidebar()

st.title("🚨 Absences & Retards")
role = st.session_state.get("role")
user_id = st.session_state.get("user_id")
student_id = st.session_state.get("student_id", user_id)

# --- Consultation ---
st.subheader("Historique des absences")
target_id = st.number_input("ID de l'élève", min_value=1, step=1, value=student_id)

if st.button("Charger"):
    absences = get(f"/api/absences/student/{target_id}")
    if absences:
        df = pd.DataFrame(absences)
        status_colors = {
            "En attente": "🟡",
            "Justifiée": "🟢",
            "Non justifiée": "🔴",
        }
        df["status"] = df["status"].map(lambda s: f"{status_colors.get(s, '')} {s}")
        df["is_late"] = df["is_late"].map({True: "Retard", False: "Absence"})
        st.dataframe(
            df[["is_late", "start_at", "end_at", "status", "reason"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "is_late": "Type",
                "start_at": "Début",
                "end_at": "Fin",
                "status": "Statut",
                "reason": "Motif",
            },
        )
    else:
        st.info("Aucune absence enregistrée.")

# --- Signalement (prof/admin) ---
if role in ("teacher", "admin"):
    st.divider()
    st.subheader("Signaler une absence")
    with st.form("absence_form"):
        s_id = st.number_input("ID de l'élève", min_value=1, step=1)
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Date de début", value=date.today())
            start_time = st.time_input("Heure de début", value=time(8, 0))
        with col2:
            end_date = st.date_input("Date de fin", value=date.today())
            end_time = st.time_input("Heure de fin", value=time(9, 0))
        is_late = st.checkbox("Retard uniquement")
        reason = st.text_area("Motif (optionnel)")
        submitted = st.form_submit_button("Enregistrer")

    if submitted:
        start = datetime.combine(start_date, start_time)
        end = datetime.combine(end_date, end_time)
        result = post("/api/absences/", {
            "student_id": s_id,
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "is_late": is_late,
            "reason": reason or None,
        })
        if result:
            st.success("Absence enregistrée ✓")

# --- Justification (parent/admin) ---
if role in ("parent", "admin"):
    st.divider()
    st.subheader("Justifier une absence")
    with st.form("justify_form"):
        abs_id = st.number_input("ID de l'absence", min_value=1, step=1)
        reason = st.text_area("Motif de justification")
        submitted = st.form_submit_button("Justifier")

    if submitted and reason:
        result = patch(f"/api/absences/{abs_id}/justify", {"reason": reason})
        if result:
            st.success("Absence justifiée ✓")
