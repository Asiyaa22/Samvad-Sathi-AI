from fastapi import FastAPI
from users.routes import router as users_router
from sessions.routes import router as sessions_router
from interviews.routes import router as interviews_router
from reports.routes import router as report_router
from sqlalchemy import text

app = FastAPI()

# include user routers
app.include_router(users_router)

#include sessions router
app.include_router(sessions_router)

#include interview routers
app.include_router(interviews_router, prefix="/interviews")
# app.include_router(interview_router, prefix="/interview", tags=["Interview"])


# app.include_router(report_router)


# root route
@app.get("/")
def read_root():
    print("hii there")
    return {"Hello": "World"}

# create tables on startup (if not using alembic)
from database import Base, engine
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

Base.metadata.create_all(bind=engine)

# def reset_database():
#     """⚠️ Dev-only: drops all tables and recreates schema fresh."""
#     with engine.connect() as conn:
#         conn.execute(text("DROP SCHEMA public CASCADE;"))
#         conn.execute(text("CREATE SCHEMA public;"))
#     Base.metadata.create_all(bind=engine)
#     print("✅ Database schema reset successfully")

# # Call it once at startup
# reset_database()
