# 🎓 Pronote 2.0

Plateforme de gestion scolaire open-source développée en Python — alternative légère et personnalisable à PRONOTE.  
Backend **FastAPI** · Frontend **Streamlit** · Base de données **PostgreSQL** · Auth **JWT**

---

## 📋 Fonctionnalités

| Module | Élève | Parent | Enseignant | Admin |
|---|:---:|:---:|:---:|:---:|
| 📅 Emploi du temps | ✅ | ✅ | ✅ | ✅ |
| 📝 Notes & évaluations | ✅ lecture | ✅ lecture | ✅ saisie | ✅ |
| 📚 Cahier de textes | ✅ | ✅ | ✅ saisie | ✅ |
| 📩 Messagerie interne | ✅ | ✅ | ✅ | ✅ |
| 🚨 Absences & retards | ✅ | ✅ justif. | ✅ signalement | ✅ |
| 📊 Bulletins scolaires | ✅ | ✅ | ✅ appréciation | ✅ |

---

## 🏗️ Architecture

```
pronote 2.0/
├── backend/                    # API REST FastAPI
│   ├── main.py                 # Point d'entrée + CORS
│   ├── config.py               # Settings (Pydantic)
│   ├── database.py             # Engine SQLAlchemy async
│   ├── dependencies.py         # Auth JWT + contrôle de rôle
│   ├── auth/
│   │   ├── router.py           # POST /api/auth/token
│   │   ├── schemas.py          # Token, LoginRequest
│   │   └── utils.py            # hash_password, create_access_token
│   ├── models/                 # Modèles SQLAlchemy (ORM)
│   │   ├── user.py             # User (4 rôles)
│   │   ├── classe.py           # Classe + association élèves
│   │   ├── subject.py          # Matières
│   │   ├── schedule.py         # Emploi du temps
│   │   ├── grade.py            # Notes & évaluations
│   │   ├── homework.py         # Cahier de textes
│   │   ├── message.py          # Messagerie
│   │   ├── absence.py          # Absences & retards
│   │   └── bulletin.py         # Bulletins & SubjectReport
│   ├── routers/                # Endpoints REST
│   │   ├── grades.py           # GET/POST/DELETE /api/grades/
│   │   ├── absences.py         # GET/POST/PATCH /api/absences/
│   │   ├── messages.py         # GET/POST/PATCH /api/messages/
│   │   ├── homework.py         # GET/POST/DELETE /api/homework/
│   │   └── schedule.py         # GET/POST /api/schedule/
│   └── schemas/                # Schémas Pydantic (validation I/O)
├── frontend/                   # Interface Streamlit
│   ├── app.py                  # Tableau de bord principal
│   ├── pages/
│   │   ├── 1_📅_Emploi_du_temps.py
│   │   ├── 2_📝_Notes.py
│   │   ├── 3_📚_Cahier_de_textes.py
│   │   ├── 4_📩_Messagerie.py
│   │   ├── 5_🚨_Absences.py
│   │   └── 6_📊_Bulletins.py
│   ├── components/
│   │   ├── auth.py             # Login / session / require_auth()
│   │   └── sidebar.py          # Navigation + profil
│   └── api/
│       └── client.py           # HTTP client vers FastAPI
├── alembic/                    # Migrations de base de données
├── tests/                      # Tests pytest-asyncio
├── .github/workflows/ci.yml    # CI GitHub Actions
├── docker-compose.yml          # Stack complète (DB + API + UI)
├── Dockerfile.backend
├── Dockerfile.frontend
├── requirements.txt
└── .env.example
```

---

## ⚙️ Stack technique

- **Python 3.12**
- **FastAPI 0.115** — API REST asynchrone, doc Swagger auto sur `/docs`
- **SQLAlchemy 2.0** — ORM async avec `asyncpg`
- **Alembic** — migrations de schéma
- **PostgreSQL 16** — base de données principale
- **Pydantic v2** — validation des données
- **python-jose + passlib** — JWT + bcrypt
- **Streamlit 1.39** — interface web
- **Plotly** — graphiques interactifs
- **Docker Compose** — orchestration locale

---

## 🚀 Installation

### Prérequis

- Python 3.12+
- PostgreSQL 16+ (ou Docker)
- pip

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-compte/pronote-2.0.git
cd pronote-2.0
```

### 2. Environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows
```

### 3. Dépendances

```bash
pip install -r requirements.txt
```

### 4. Variables d'environnement

```bash
cp .env.example .env
# Éditer .env avec tes valeurs (DATABASE_URL, SECRET_KEY…)
```

### 5. Base de données

```bash
# Avec Docker (recommandé)
docker run -d \
  --name pronote_db \
  -e POSTGRES_USER=pronote \
  -e POSTGRES_PASSWORD=pronote \
  -e POSTGRES_DB=pronote_db \
  -p 5432:5432 \
  postgres:16-alpine

# Migrations
alembic upgrade head
```

### 6. Lancer l'application

**Terminal 1 — Backend API**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 — Frontend Streamlit**
```bash
streamlit run frontend/app.py --server.port 8501
```

Ouvrir [http://localhost:8501](http://localhost:8501)

---

## 🐳 Démarrage avec Docker Compose

Lance l'ensemble de la stack en une seule commande :

```bash
docker-compose up --build
```

| Service | URL |
|---|---|
| Frontend Streamlit | http://localhost:8501 |
| Backend API | http://localhost:8000 |
| Swagger (doc API) | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

---

## 🔑 Authentification

L'API utilise **OAuth2 + JWT Bearer**.

```bash
# Obtenir un token
curl -X POST http://localhost:8000/api/auth/token \
  -d "username=admin@school.fr&password=password"

# Utiliser le token
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/grades/student/1
```

### Rôles disponibles

| Rôle | Accès |
|---|---|
| `admin` | Lecture + écriture sur tout |
| `teacher` | Saisie notes, devoirs, signalement absences |
| `student` | Lecture de ses propres données |
| `parent` | Lecture + justification des absences |

---

## 🧪 Tests

```bash
# Lancer tous les tests
pytest tests/ -v

# Avec coverage
pytest tests/ --cov=backend --cov-report=html
```

---

## 🗄️ Migrations

```bash
# Générer une migration après modification des modèles
alembic revision --autogenerate -m "description"

# Appliquer les migrations
alembic upgrade head

# Revenir en arrière
alembic downgrade -1
```

---

## 📡 Endpoints API

| Méthode | Route | Rôle requis | Description |
|---|---|---|---|
| POST | `/api/auth/token` | — | Connexion |
| GET | `/api/grades/student/{id}` | Tous | Notes d'un élève |
| POST | `/api/grades/` | teacher, admin | Saisir une note |
| DELETE | `/api/grades/{id}` | teacher, admin | Supprimer une note |
| GET | `/api/absences/student/{id}` | Tous | Absences d'un élève |
| POST | `/api/absences/` | teacher, admin | Signaler une absence |
| PATCH | `/api/absences/{id}/justify` | parent, admin | Justifier une absence |
| GET | `/api/messages/inbox` | Tous | Messages reçus |
| GET | `/api/messages/sent` | Tous | Messages envoyés |
| POST | `/api/messages/` | Tous | Envoyer un message |
| PATCH | `/api/messages/{id}/read` | Tous | Marquer comme lu |
| GET | `/api/homework/classe/{id}` | Tous | Devoirs d'une classe |
| POST | `/api/homework/` | teacher, admin | Publier un devoir |
| GET | `/api/schedule/classe/{id}` | Tous | EDT d'une classe |
| POST | `/api/schedule/` | admin | Créer un créneau |

Documentation interactive complète : **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 🗺️ Roadmap

- [ ] Gestion complète des bulletins (génération PDF)
- [ ] Notifications temps réel (WebSockets)
- [ ] Interface administration (gestion classes, utilisateurs)
- [ ] Export Excel des notes
- [ ] Application mobile (API déjà prête)
- [ ] Système de permissions granulaires
- [ ] Intégration ENT

---

## 🤝 Contribution

1. Fork le projet
2. Crée une branche : `git checkout -b feature/ma-fonctionnalite`
3. Commit : `git commit -m "feat: description"`
4. Push : `git push origin feature/ma-fonctionnalite`
5. Ouvre une Pull Request

---

## 📄 Licence

MIT — libre d'utilisation, modification et distribution.

---

*Développé par Alexandre PAVIEL — LaBlackBox Studio / En Studio*
