import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import streamlit as st
from frontend.components.auth import require_auth
from frontend.components.sidebar import render_sidebar
from frontend.api.client import get, post, patch

st.set_page_config(page_title="Messagerie", page_icon="📩", layout="wide")
require_auth()
render_sidebar()

st.title("📩 Messagerie")

tab_inbox, tab_sent, tab_compose = st.tabs(["📥 Reçus", "📤 Envoyés", "✏️ Nouveau message"])

with tab_inbox:
    messages = get("/api/messages/inbox") or []
    if not messages:
        st.info("Aucun message reçu.")
    for msg in messages:
        read_icon = "🔵" if not msg["is_read"] else "⚪"
        with st.expander(f"{read_icon} **{msg['subject']}** — de #{msg['sender_id']}  |  {msg['sent_at'][:10]}"):
            st.write(msg["body"])
            if not msg["is_read"]:
                if st.button("Marquer comme lu", key=f"read_{msg['id']}"):
                    patch(f"/api/messages/{msg['id']}/read")
                    st.rerun()

with tab_sent:
    sent = get("/api/messages/sent") or []
    if not sent:
        st.info("Aucun message envoyé.")
    for msg in sent:
        with st.expander(f"**{msg['subject']}** — à #{msg['recipient_id']}  |  {msg['sent_at'][:10]}"):
            st.write(msg["body"])

with tab_compose:
    with st.form("compose_form"):
        recipient_id = st.number_input("ID du destinataire", min_value=1, step=1)
        subject = st.text_input("Objet")
        body = st.text_area("Message", height=200)
        submitted = st.form_submit_button("Envoyer", use_container_width=True)

    if submitted and subject and body:
        result = post("/api/messages/", {
            "recipient_id": recipient_id,
            "subject": subject,
            "body": body,
        })
        if result:
            st.success("Message envoyé ✓")
