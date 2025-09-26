from fastapi import FastAPI

from .api import admin, auth, events
from .core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Local Skill-Sharing Event Platform API")

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(admin.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Local Skill-Sharing Event Platform API"}
