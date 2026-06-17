from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str = Field(min_length=6)


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str


class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    cargo: str

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioOut

class ClassePersonagem(str, Enum):
    combatente = "Combatente"
    especialista = "Especialista"
    ocultista = "Ocultista"


class Atributos(BaseModel):
    agilidade: int = 1
    forca: int = 1
    intelecto: int = 1
    presenca: int = 1
    vigor: int = 1


class Recurso(BaseModel):
    atual: int
    maximo: int


class Pericia(BaseModel):
    nome: str
    treinada: bool = False


class FichaDados(BaseModel):
    imagem: Optional[str] = None
    classe: ClassePersonagem
    origem: str
    trilha: Optional[str] = None
    nex: int = Field(default=5, ge=5, le=99)

    atributos: Atributos
    pontos_de_vida: Recurso
    pontos_de_esforco: Recurso
    sanidade: Recurso

    pericias: List[Pericia] = Field(default_factory=list)
    poderes: List[str] = Field(default_factory=list)
    rituais: List[str] = Field(default_factory=list)
    inventario: List[str] = Field(default_factory=list)
    historia: str = ""


class FichaCreate(BaseModel):
    nome: str
    dados_da_ficha: FichaDados


class FichaUpdate(BaseModel):
    nome: Optional[str] = None
    dados_da_ficha: Optional[FichaDados] = None


class FichaOut(BaseModel):
    id: int
    nome: str
    dados_da_ficha: FichaDados
    criador_id: int
    data_criacao: datetime

    class Config:
        from_attributes = True
