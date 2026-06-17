from fastapi import APIRouter

import schemas

router = APIRouter(tags=["Opções"])


@router.get("/opcoes")
def listar_opcoes():
    
    return {
        "classes": [c.value for c in schemas.ClassePersonagem],
        "atributos": ["agilidade", "forca", "intelecto", "presenca", "vigor"],
    }
