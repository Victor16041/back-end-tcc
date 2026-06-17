from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import auth

router = APIRouter(prefix="/fichas", tags=["Fichas"])


def _buscar_ficha_ou_404(ficha_id: int, db: Session) -> models.Ficha:
    ficha = db.query(models.Ficha).filter(models.Ficha.id == ficha_id).first()
    if not ficha:
        raise HTTPException(status_code=404, detail="ficha não encontrada")
    return ficha


def _checar_permissao(ficha: models.Ficha, usuario: models.Usuario):
    if usuario.cargo != "admin" and ficha.criador_id != usuario.id:
        raise HTTPException(status_code=403, detail="acesso negado a esta ficha")


@router.get("", response_model=List[schemas.FichaOut])
def listar_fichas(
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(auth.get_usuario_atual),
):
    if usuario.cargo == "admin":
        return db.query(models.Ficha).all()
    return db.query(models.Ficha).filter(models.Ficha.criador_id == usuario.id).all()


@router.post("", response_model=schemas.FichaOut, status_code=status.HTTP_201_CREATED)
def criar_ficha(
    dados: schemas.FichaCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(auth.get_usuario_atual),
):
    ficha = models.Ficha(
        nome=dados.nome,
        dados_da_ficha=dados.dados_da_ficha.model_dump(mode="json"),
        criador_id=usuario.id,
    )
    db.add(ficha)
    db.commit()
    db.refresh(ficha)
    return ficha


@router.get("/{ficha_id}", response_model=schemas.FichaOut)
def ver_ficha(
    ficha_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(auth.get_usuario_atual),
):
    ficha = _buscar_ficha_ou_404(ficha_id, db)
    _checar_permissao(ficha, usuario)
    return ficha


@router.put("/{ficha_id}", response_model=schemas.FichaOut)
def editar_ficha(
    ficha_id: int,
    dados: schemas.FichaUpdate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(auth.get_usuario_atual),
):
    ficha = _buscar_ficha_ou_404(ficha_id, db)
    _checar_permissao(ficha, usuario)

    if dados.nome is not None:
        ficha.nome = dados.nome
    if dados.dados_da_ficha is not None:
        ficha.dados_da_ficha = dados.dados_da_ficha.model_dump(mode="json")

    db.commit()
    db.refresh(ficha)
    return ficha


@router.delete("/{ficha_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_ficha(
    ficha_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(auth.get_usuario_atual),
):
    ficha = _buscar_ficha_ou_404(ficha_id, db)
    _checar_permissao(ficha, usuario)
    db.delete(ficha)
    db.commit()
