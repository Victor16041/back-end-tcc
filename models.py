from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    cargo = Column(String, default="usuario", nullable=False)

    fichas = relationship("Ficha", back_populates="criador", cascade="all, delete-orphan")


class Ficha(Base):
    __tablename__ = "fichas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    dados_da_ficha = Column(JSON, nullable=False, default=dict)

    criador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow, nullable=False)

    criador = relationship("Usuario", back_populates="fichas")
