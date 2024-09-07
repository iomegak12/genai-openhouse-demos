from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_FILE = "data.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///.{DB_FILE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={
                           "check_same_thread": False
                       },
                       echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
