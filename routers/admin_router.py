from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import auth

router = APIRouter(prefix="/admin", tags=["administração"])


@router.get("/usuarios", response_model=List[schemas.UsuarioOut])
def listar_usuarios(
    db: Session = Depends(get_db),
    _admin: models.Usuario = Depends(auth.exigir_admin),
):
    return db.query(models.Usuario).all()


@router.get("/fichas", response_model=List[schemas.FichaOut])
def listar_todas_fichas(
    db: Session = Depends(get_db),
    _admin: models.Usuario = Depends(auth.exigir_admin),
):
    return db.query(models.Ficha).all()
