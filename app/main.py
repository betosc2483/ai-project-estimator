
from fastapi import FastAPI
from app.routers import estimations


app = FastAPI(
    title="Estimador CAG - LIDR",
    description="API para estimar proyectos de software utilizando CAG y Claude",
    version="0.1.0"
)

app.include_router(estimations.router)


@app.get("/health")
async def health():
    return {"status": "healthy"}
