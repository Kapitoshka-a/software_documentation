from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from controllers import MessageController
from core.config import settings
from data_access import MessageRepository
from routers.client_web import router as client_router
from routers.operator_web import router as operator_router
from routers.home_web import router as home_router

app = FastAPI()

@app.get("/health")
def health():
    return 200

origins = [
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/messages")
def root(conversation_id: str, session = Depends(settings.get_sqlite_session)) -> dict:
    repository = MessageRepository(session)
    messages = MessageController(repository).list_messages(conversation_id=conversation_id)
    return dict(
        messages = messages
    )

app.include_router(client_router)
app.include_router(operator_router)
app.include_router(home_router)