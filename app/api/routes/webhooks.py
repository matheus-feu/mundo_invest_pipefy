from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.services.webhook_service import WebhookService
from app.infrastructure.database.repositories.sql_client_repository import SQLClientRepository
from app.infrastructure.database.repositories.sql_webhook_repository import SQLWebhookRepository
from app.infrastructure.integrations.pipefy.graphql_client import PipefyGraphQLClient
from app.schemas.webhook import PipefyWebhook

webhook_router = APIRouter()


def get_webhook_service(db: Session = Depends(get_db)) -> WebhookService:
	client_repo = SQLClientRepository(db)
	webhook_repo = SQLWebhookRepository(db)
	graphql_client = PipefyGraphQLClient()
	return WebhookService(client_repo, webhook_repo, graphql_client)

@webhook_router.post("/pipefy/card-updated")
def card_updated(
		payload: PipefyWebhook,
		service: WebhookService = Depends(get_webhook_service),
):
	return service.process_card_updated(payload)
