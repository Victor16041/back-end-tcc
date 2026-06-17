from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import auth

router = APIRouter(tags=["autenticação"])


@router.post("/cadastro", response_model=schemas.TokenOut, status_code=status.HTTP_201_CREATED)
def cadastro(dados: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    email_existente = db.query(models.Usuario).filter(models.Usuario.email == dados.email).first()
    if email_existente:
        raise HTTPException(status_code=400, detail="e-mail já cadastrado")

    usuario = models.Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=auth.hash_senha(dados.senha),
        cargo="usuario",
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    token = auth.criar_token({"usuario_id": usuario.id, "cargo": usuario.cargo})
    return schemas.TokenOut(access_token=token, usuario=usuario)


@router.post("/login", response_model=schemas.TokenOut)
def login(dados: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == dados.email).first()
    if not usuario or not auth.verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="e-mail ou senha incorretos")

    token = auth.criar_token({"usuario_id": usuario.id, "cargo": usuario.cargo})
    return schemas.TokenOut(access_token=token, usuario=usuario)
