"""Client HTTP vers l'API FastAPI."""
from typing import Dict, List, Optional, Union

import requests
import streamlit as st
from frontend.api.mock import demo_get, demo_login, demo_patch, demo_post

API_URL = "http://localhost:8000"


def get_headers() -> Dict[str, str]:
    token = st.session_state.get("token", "")
    return {"Authorization": f"Bearer {token}"}


def login(email: str, password: str) -> Optional[Dict]:
    if email == "demo@pronote.local" and password == "demo":
        st.session_state["demo_mode"] = True
        return demo_login()
    try:
        resp = requests.post(
            f"{API_URL}/api/auth/token",
            data={"username": email, "password": password},
            timeout=10,
        )
        if resp.status_code == 200:
            return resp.json()
        st.error(resp.json().get("detail", "Erreur de connexion"))
        return None
    except requests.exceptions.ConnectionError:
        st.error("Impossible de joindre l'API. Vérifiez que le backend est démarré.")
        return None


def get(endpoint: str, params: Optional[Dict] = None) -> Optional[Union[List, Dict]]:
    if st.session_state.get("demo_mode"):
        return demo_get(endpoint)
    try:
        resp = requests.get(f"{API_URL}{endpoint}", headers=get_headers(), params=params, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        st.error(f"Erreur {resp.status_code} : {resp.json().get('detail', '')}")
        return None
    except requests.exceptions.ConnectionError:
        st.error("API inaccessible.")
        return None


def post(endpoint: str, data: Dict) -> Optional[Dict]:
    if st.session_state.get("demo_mode"):
        return demo_post(endpoint, data)
    try:
        resp = requests.post(f"{API_URL}{endpoint}", headers=get_headers(), json=data, timeout=10)
        if resp.status_code in (200, 201):
            return resp.json()
        st.error(f"Erreur {resp.status_code} : {resp.json().get('detail', '')}")
        return None
    except requests.exceptions.ConnectionError:
        st.error("API inaccessible.")
        return None


def patch(endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
    if st.session_state.get("demo_mode"):
        return demo_patch(endpoint, data)
    try:
        resp = requests.patch(f"{API_URL}{endpoint}", headers=get_headers(), json=data, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        st.error(f"Erreur {resp.status_code}")
        return None
    except requests.exceptions.ConnectionError:
        st.error("API inaccessible.")
        return None
