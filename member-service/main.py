from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="Member Service",
    description="""
## Library Management System — Member Service

Handles all library member operations including registration,
profile management, membership status, and member lookup.

### Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/members/ | Register new member |
| GET | /api/members/ | Get all members |
| GET | /api/members/{id} | Get member by ID |
| GET | /api/members/status/{status} | Filter by status |
| GET | /api/members/type/{type} | Filter by membership type |
| PUT | /api/members/{id} | Update member |
| PATCH | /api/members/{id}/suspend | Suspend member |
| PATCH | /api/members/{id}/activate | Activate member |
| DELETE | /api/members/{id} | Delete member |
    """,
    version="1.0.0"
)

app.include_router(router)


@app.get("/", tags=["Health"])
def root():
    return {
        "service": "Member Service",
        "status": "running",
        "docs": "http://localhost:8002/docs"
    }
