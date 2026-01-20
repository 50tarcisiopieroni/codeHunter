from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from models.ArquivosMonitorado import Base

engine = create_engine(Config.DB_NAME, echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Cria as tabelas se não existirem"""
    Base.metadata.create_all(engine)

def get_db():
    """Retorna uma nova sessão"""
    return SessionLocal()