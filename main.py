from fastapi import FastAPI

from app.api.routes.clients import clients_router
from app.api.routes.webhooks import webhook_router
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
	title="Mundo Invest API",
	description="API para gerenciamento de clientes e processamento de webhooks do Pipefy.",
	version="1.0.0",
	docs_url="/api/v1/docs",
	redoc_url="/api/v1/redoc",
	openapi_url="/api/v1/openapi.json"
)
app.include_router(clients_router, prefix="/api/v1", tags=["Clientes"])
app.include_router(webhook_router, prefix="/api/v1/webhooks", tags=["Webhooks"])

if __name__ == "__main__":
	import uvicorn

	uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
