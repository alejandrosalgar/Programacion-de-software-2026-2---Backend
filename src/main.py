


app = FastAPI(
    title="API Banco — Programacion de software 2026-2",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en desarrollo; luego el origen real del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios_router)
app.include_router(cuentas_router)
app.include_router(tarjetas_router)


@app.get("/")
def raiz():
    return {"mensaje": "API en marcha"}