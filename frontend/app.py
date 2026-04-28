"""
Pronote 2.0 — Tableau de bord principal
Point d'entrée Streamlit : affiche la page de login ou le dashboard selon la session.
"""
import streamlit as st
from datetime import datetime

# ── Config page (doit être le 1er appel Streamlit) ──────────────────────────
st.set_page_config(
    page_title="Pronote 2.0",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "Pronote 2.0 — Plateforme scolaire open-source",
    },
)

# ── CSS personnalisé ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Cartes métriques */
    [data-testid="metric-container"] {
        background: #f8f9fc;
        border: 1px solid #e3e8f0;
        border-radius: 12px;
        padding: 16px 20px;
    }
    [data-testid="metric-container"] [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        color: #6b7280;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
    }

    /* Titre principal */
    h1 { color: #1e293b !important; }

    /* Boutons d'accès rapide */
    .stPageLink > a {
        border: 1px solid #e3e8f0 !important;
        border-radius: 10px !important;
        padding: 12px !important;
        transition: all 0.2s ease;
    }
    .stPageLink > a:hover {
        border-color: #3b82f6 !important;
        background: #eff6ff !important;
    }

    /* Masquer le menu hamburger par défaut */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Imports internes (après set_page_config) ─────────────────────────────────
from frontend.components.auth import require_auth, show_login_page, is_logged_in
from frontend.components.sidebar import render_sidebar
from frontend.api.client import get


# ── Login ─────────────────────────────────────────────────────────────────────
if not is_logged_in():
    # Page de connexion centrée et stylée
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align:center; margin-bottom: 2rem;">
                <span style="font-size: 3.5rem;">🎓</span>
                <h1 style="margin: 0.5rem 0 0.25rem; color: #1e293b;">Pronote 2.0</h1>
                <p style="color: #6b7280; font-size: 0.95rem;">
                    Plateforme de gestion scolaire
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        show_login_page()
    st.stop()


# ── Dashboard (utilisateur connecté) ─────────────────────────────────────────
render_sidebar()

role = st.session_state.get("role", "")
user_id = st.session_state.get("user_id")
student_id = st.session_state.get("student_id", user_id)
full_name = st.session_state.get("full_name", "")

ROLE_LABELS = {
    "admin": ("🏫", "Administration"),
    "teacher": ("👨‍🏫", "Enseignant"),
    "student": ("👨‍🎓", "Élève"),
    "parent": ("👨‍👩‍👧", "Parent"),
}
role_icon, role_label = ROLE_LABELS.get(role, ("👤", role))

# ── En-tête ───────────────────────────────────────────────────────────────────
col_title, col_date = st.columns([3, 1])
with col_title:
    st.markdown(f"# {role_icon} Tableau de bord")
    st.caption(f"Connecté en tant que **{full_name}** · {role_label}")
with col_date:
    st.markdown("<br>", unsafe_allow_html=True)
    now = datetime.now()
    st.markdown(
        f"<p style='text-align:right; color:#6b7280; font-size:0.85rem;'>"
        f"{now.strftime('%A %d %B %Y').capitalize()}<br>"
        f"<strong>{now.strftime('%H:%M')}</strong></p>",
        unsafe_allow_html=True,
    )

st.divider()

# ── KPIs (chargement des données) ─────────────────────────────────────────────
inbox = get("/api/messages/inbox") or []
unread_count = sum(1 for m in inbox if not m.get("is_read"))

absences_data = []
pending_absences = 0
grades_data = []

if role in ("student", "parent"):
    absences_data = get(f"/api/absences/student/{student_id}") or []
    pending_absences = sum(1 for a in absences_data if a.get("status") == "En attente")
    grades_data = get(f"/api/grades/student/{student_id}") or []

# ── Métriques selon le rôle ───────────────────────────────────────────────────
if role in ("student", "parent"):
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("📩 Messages non lus", unread_count,
                  delta=f"-{unread_count}" if unread_count else None,
                  delta_color="inverse")
    with k2:
        st.metric("🚨 Absences en attente", pending_absences,
                  delta="à justifier" if pending_absences else None,
                  delta_color="inverse" if pending_absences else "off")
    with k3:
        total_abs = len(absences_data)
        justified = sum(1 for a in absences_data if a.get("status") == "Justifiée")
        st.metric("📋 Total absences", total_abs, delta=f"{justified} justifiées", delta_color="off")
    with k4:
        nb_grades = len(grades_data)
        if grades_data:
            avg = sum(g["value"] / g["max_value"] * 20 for g in grades_data) / nb_grades
            st.metric("📝 Moyenne générale", f"{avg:.1f}/20", delta=f"{nb_grades} notes")
        else:
            st.metric("📝 Notes enregistrées", nb_grades)

elif role == "teacher":
    k1, k2 = st.columns(2)
    with k1:
        st.metric("📩 Messages non lus", unread_count)
    with k2:
        st.metric("📚 Espace enseignant", "Actif", delta="Connecté")

elif role == "admin":
    k1, k2 = st.columns(2)
    with k1:
        st.metric("📩 Messages non lus", unread_count)
    with k2:
        st.metric("🏫 Mode", "Administration", delta="Accès complet")

st.divider()

# ── Graphiques (élève/parent) ─────────────────────────────────────────────────
if role in ("student", "parent") and grades_data:
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go

    df_grades = pd.DataFrame(grades_data)
    df_grades["note_20"] = (df_grades["value"] / df_grades["max_value"] * 20).round(2)
    df_grades["graded_at"] = pd.to_datetime(df_grades["graded_at"])
    df_grades = df_grades.sort_values("graded_at")

    col_chart1, col_chart2 = st.columns([2, 1])

    with col_chart1:
        st.subheader("📈 Évolution des notes")
        fig_line = px.line(
            df_grades,
            x="graded_at",
            y="note_20",
            text="note_20",
            markers=True,
            labels={"graded_at": "", "note_20": "Note /20"},
            color_discrete_sequence=["#3b82f6"],
        )
        fig_line.add_hline(
            y=10, line_dash="dot", line_color="#ef4444",
            annotation_text="Seuil 10", annotation_position="bottom right",
        )
        fig_line.add_hrect(y0=14, y1=20, fillcolor="#22c55e", opacity=0.05, line_width=0)
        fig_line.update_traces(textposition="top center", textfont_size=11)
        fig_line.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor="white",
            paper_bgcolor="white",
            yaxis=dict(range=[0, 21], gridcolor="#f1f5f9"),
            xaxis=dict(gridcolor="#f1f5f9"),
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with col_chart2:
        st.subheader("📊 Répartition")
        bins = {"< 8": 0, "8-10": 0, "10-14": 0, "14-16": 0, "≥ 16": 0}
        for n in df_grades["note_20"]:
            if n < 8:
                bins["< 8"] += 1
            elif n < 10:
                bins["8-10"] += 1
            elif n < 14:
                bins["10-14"] += 1
            elif n < 16:
                bins["14-16"] += 1
            else:
                bins["≥ 16"] += 1

        fig_pie = go.Figure(go.Pie(
            labels=list(bins.keys()),
            values=list(bins.values()),
            hole=0.5,
            marker_colors=["#ef4444", "#f97316", "#3b82f6", "#22c55e", "#8b5cf6"],
            textinfo="label+percent",
        ))
        fig_pie.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            showlegend=False,
            paper_bgcolor="white",
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()

# ── Derniers messages (aperçu) ────────────────────────────────────────────────
if inbox:
    st.subheader("📩 Derniers messages reçus")
    preview = inbox[:3]
    for msg in preview:
        read_dot = "🔵" if not msg.get("is_read") else "⚪"
        date_str = msg.get("sent_at", "")[:10]
        with st.container(border=True):
            col_dot, col_info = st.columns([0.05, 0.95])
            with col_dot:
                st.markdown(f"<p style='font-size:1.2rem;margin-top:4px'>{read_dot}</p>", unsafe_allow_html=True)
            with col_info:
                st.markdown(f"**{msg.get('subject', '(sans objet)')}**  ·  <span style='color:#6b7280;font-size:0.8rem'>{date_str}</span>", unsafe_allow_html=True)
                body_preview = msg.get("body", "")[:120]
                if len(msg.get("body", "")) > 120:
                    body_preview += "…"
                st.caption(body_preview)

    if len(inbox) > 3:
        st.page_link("pages/4_📩_Messagerie.py", label=f"Voir tous les messages ({len(inbox)})")

    st.divider()

# ── Accès rapide ──────────────────────────────────────────────────────────────
st.subheader("🚀 Accès rapide")

pages = [
    ("pages/1_📅_Emploi_du_temps.py", "📅 Emploi du temps"),
    ("pages/2_📝_Notes.py", "📝 Notes"),
    ("pages/3_📚_Cahier_de_textes.py", "📚 Cahier de textes"),
    ("pages/4_📩_Messagerie.py", "📩 Messagerie"),
    ("pages/5_🚨_Absences.py", "🚨 Absences"),
    ("pages/6_📊_Bulletins.py", "📊 Bulletins"),
]

cols = st.columns(len(pages))
for col, (path, label) in zip(cols, pages):
    with col:
        st.page_link(path, label=label, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#94a3b8; font-size:0.75rem;'>"
    "Pronote 2.0 · Plateforme scolaire open-source · "
    "<a href='http://localhost:8000/docs' target='_blank' style='color:#3b82f6;'>API Docs</a>"
    "</p>",
    unsafe_allow_html=True,
)
