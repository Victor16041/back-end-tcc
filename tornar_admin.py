import sys
from database import SessionLocal
import models

def tornar_admin(email: str):
    db = SessionLocal()
    try:
        usuario = db.query(models.Usuario).filter(models.Usuario.email == email).first()
        if not usuario:
            print(f"nenhum usuário encontrado com o e-mail: {email}")
            return
        usuario.cargo = "admin"
        db.commit()
        print(f"{usuario.nome} ({usuario.email}) agora é admin.")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("uso: python tornar_admin.py email@exemplo.com")
        sys.exit(1)
    tornar_admin(sys.argv[1])
