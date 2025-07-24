from fastapi import FastAPI
from users.routes import router as users_router
from sessions.routes import router as sessions_router
from interviews.routes import router as interviews_router

app = FastAPI()

# include user routers
app.include_router(users_router, prefix="/users")

#include sessions router
app.include_router(sessions_router, prefix="/sessions")

#include interview routers
app.include_router(interviews_router, prefix="/api/interviews")
# app.include_router(interview_router, prefix="/interview", tags=["Interview"])

# root route
@app.get("/")
def read_root():
    return {"Hello": "World"}

# create tables on startup (if not using alembic)
from database import Base, engine
Base.metadata.create_all(bind=engine)
