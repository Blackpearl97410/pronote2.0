import streamlit as st
import pandas as pd
from frontend.components.auth import require_auth
from frontend.components.sidebar import render_sidebar
from frontend.api.client import get

st.set_page_config(page_title="Emploi du temps", page_icon="📅", layout="wide")
require_auth()
render_sidebar()

st.title("📅 Emploi du temps")

classe_id = st.number_input("ID de la classe", min_value=1, step=1, value=1)

if st.button("Charger"):
    slots = get(f"/api/schedule/classe/{classe_id}")
    if slots:
        df = pd.DataFrame(slots)
        df = df[["day_of_week", "start_time", "end_time", "room", "subject_id", "teacher_id", "is_cancelled"]]
        df.columns = ["Jour", "Début", "Fin", "Salle", "Matière (ID)", "Professeur (ID)", "Annulé"]
        df = df.sort_values(["Jour", "Début"])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucun créneau trouvé pour cette classe.")
