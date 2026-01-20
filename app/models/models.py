from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, Field

Base = declarative_base()

class ArquivoMonitorado(Base):
    __tablename__ = 'arquivo_monitorado'
    
    id = Column(Integer, primary_key=True)
    file_path = Column(String, unique=True, nullable=False)
    last_commit_sha = Column(String, nullable=False)
    last_analyzed_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String)  # 'CLEAN', 'ISSUES_FOUND'

class AnalysisResult(BaseModel):
    has_smell: bool = Field(description="True se detectar code smell")
    smell_type: str = Field(description="Nome do padrão (ex: God Class, Long Method)")
    severity: str = Field(description="Baixa, Media ou Alta")
    description: str = Field(description="Explicação do problema")
    suggestion: str = Field(description="Código refatorado sugerido")