from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import List, Tuple

# SQLite Database
DATABASE_URL = "sqlite:///./elements.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class ElementDB(Base):
    __tablename__ = "elements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    points = Column(JSON)  # Stores list of tuples as JSON

# Create the table
Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#make app
app = FastAPI()

"""Cors bypass"""
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://inter-ai.github.io/", "0.0.0.0","121.0.0.1"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

stored_list: List[str] = ["a","b","cd","efg"]

@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    print(db.query(ElementDB).get("names"))
    return db.query(ElementDB).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
run venv:
    source venv/bin/activate
run:
    uvicorn server:app --reload
"""