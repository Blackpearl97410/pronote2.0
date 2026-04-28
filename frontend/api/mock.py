"""Donnees de demonstration pour naviguer sans backend."""

from copy import deepcopy


DEMO_USER = {
    "access_token": "demo-token",
    "role": "student",
    "full_name": "Alexandre Paviel",
    "user_id": 1,
    "student_id": 1,
}


_MESSAGES_INBOX = [
    {
        "id": 1,
        "sender_id": 12,
        "recipient_id": 1,
        "subject": "Bienvenue sur Pronote 2.0",
        "body": "Voici un apercu de la messagerie interne pour le mode demo.",
        "sent_at": "2026-04-25T08:30:00",
        "is_read": False,
    },
    {
        "id": 2,
        "sender_id": 8,
        "recipient_id": 1,
        "subject": "Devoir de mathematiques",
        "body": "Pense a rendre les exercices 4 a 8 pour vendredi.",
        "sent_at": "2026-04-24T16:15:00",
        "is_read": True,
    },
]

_MESSAGES_SENT = [
    {
        "id": 3,
        "sender_id": 1,
        "recipient_id": 12,
        "subject": "Question sur le cours",
        "body": "Je voulais confirmer la date du prochain controle.",
        "sent_at": "2026-04-23T18:00:00",
        "is_read": True,
    }
]

_GRADES = [
    {
        "id": 1,
        "title": "Controle fractions",
        "grade_type": "Controle",
        "value": 15.5,
        "max_value": 20.0,
        "coefficient": 2.0,
        "appreciation": "Bon travail, ensemble solide.",
        "graded_at": "2026-04-10T09:00:00",
    },
    {
        "id": 2,
        "title": "Expression ecrite",
        "grade_type": "Devoir surveille",
        "value": 13.0,
        "max_value": 20.0,
        "coefficient": 1.0,
        "appreciation": "Des idees interessantes, attention a la structure.",
        "graded_at": "2026-04-17T09:00:00",
    },
    {
        "id": 3,
        "title": "TP sciences",
        "grade_type": "Travaux pratiques",
        "value": 17.0,
        "max_value": 20.0,
        "coefficient": 1.5,
        "appreciation": "Tres bonne participation.",
        "graded_at": "2026-04-22T14:00:00",
    },
]

_ABSENCES = [
    {
        "id": 1,
        "student_id": 1,
        "start_at": "2026-04-03T08:00:00",
        "end_at": "2026-04-03T10:00:00",
        "status": "Justifiee",
        "reason": "Rendez-vous medical",
        "is_late": False,
    },
    {
        "id": 2,
        "student_id": 1,
        "start_at": "2026-04-19T08:05:00",
        "end_at": "2026-04-19T08:20:00",
        "status": "En attente",
        "reason": "Transport en retard",
        "is_late": True,
    },
]

_SCHEDULE = [
    {
        "day_of_week": "Lundi",
        "start_time": "08:00",
        "end_time": "09:00",
        "room": "B12",
        "subject_id": 1,
        "teacher_id": 21,
        "is_cancelled": False,
    },
    {
        "day_of_week": "Lundi",
        "start_time": "10:00",
        "end_time": "11:00",
        "room": "C03",
        "subject_id": 4,
        "teacher_id": 17,
        "is_cancelled": False,
    },
    {
        "day_of_week": "Mardi",
        "start_time": "13:00",
        "end_time": "15:00",
        "room": "Lab 2",
        "subject_id": 7,
        "teacher_id": 11,
        "is_cancelled": False,
    },
]

_HOMEWORK = [
    {
        "id": 1,
        "title": "Exercices chapitre 6",
        "due_date": "2026-05-02",
        "is_graded": True,
        "description": "Faire les exercices 12 a 18 sur le cahier.",
    },
    {
        "id": 2,
        "title": "Lecture analytique",
        "due_date": "2026-05-05",
        "is_graded": False,
        "description": "Lire le texte et preparer trois axes d'analyse.",
    },
]


def demo_login() -> dict:
    return deepcopy(DEMO_USER)


def demo_get(endpoint: str):
    if endpoint == "/api/messages/inbox":
        return deepcopy(_MESSAGES_INBOX)
    if endpoint == "/api/messages/sent":
        return deepcopy(_MESSAGES_SENT)
    if endpoint.startswith("/api/grades/student/"):
        return deepcopy(_GRADES)
    if endpoint.startswith("/api/absences/student/"):
        return deepcopy(_ABSENCES)
    if endpoint.startswith("/api/schedule/classe/"):
        return deepcopy(_SCHEDULE)
    if endpoint.startswith("/api/homework/classe/"):
        return deepcopy(_HOMEWORK)
    return None


def demo_post(endpoint: str, data: dict) -> dict:
    return {"ok": True, "endpoint": endpoint, "data": deepcopy(data)}


def demo_patch(endpoint: str, data=None) -> dict:
    return {"ok": True, "endpoint": endpoint, "data": deepcopy(data)}
