import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(
        f"Falta DATABASE_URL en el archivo .env. Ruta buscada: {project_root / '.env'}"
    )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_session():
    return SessionLocal()
