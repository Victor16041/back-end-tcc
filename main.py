from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import auth_router, fichas_router, admin_router, opcoes_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="cópia barata do cris",
    description="vgsfgwefcvbdfgbf",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(fichas_router.router)
app.include_router(admin_router.router)
app.include_router(opcoes_router.router)


@app.get("/", tags=["Status"])
def raiz():
    return {"status": "online", "docs": "/docs"}
