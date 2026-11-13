from sqlalchemy import create_engine        
from sqlalchemy.orm import sessionmaker, DeclarativeBase

#database connection and session management

DATABASE_URL = "sqlite:///./taskboard.db" #sqlite database file will be created in the current directory


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase): #parent class for all models
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



