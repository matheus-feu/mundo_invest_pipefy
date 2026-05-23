from app.infrastructure.database.models.client import ClientStatus, ClientPriority
from app.infrastructure.integrations.pipefy.graphql_client import PipefyGraphQLClient
from app.schemas.webhook import PipefyWebhook


class WebhookService:
    def __init__(self, client_repository, webhook_repository, graphql_client: PipefyGraphQLClient):
        self.client_repository = client_repository
        self.webhook_repository = webhook_repository
        self.graphql_client = graphql_client

    def process_card_updated(self, payload: PipefyWebhook):
        # 1. Idempotência — tenta registrar o evento atomicamente
        registered = self.webhook_repository.register_if_not_exists(
            event_id=payload.event_id,
            card_id=payload.card_id,
            client_email=payload.cliente_email,
            timestamp=payload.timestamp,
        )
        if not registered:
            return {"message": "Evento já processado", "event_id": payload.event_id}

        # 2. Buscar cliente pelo email
        client = self.client_repository.get_client_by_email(payload.cliente_email)
        if not client:
            return {"message": "Cliente não encontrado", "cliente_email": payload.cliente_email}

        # 3. Calcular prioridade pelo patrimônio
        priority = (
            ClientPriority.high
            if client.equity_value >= 200000
            else ClientPriority.normal
        )

        # 4. Montar mutation GraphQL de update (simulado)
        graphql_payload = self.graphql_client.build_update_card_payload(card_id=payload.card_id, priority=priority)
        print("Payload para atualização de card no Pipefy:", graphql_payload)

        # 5. Atualizar banco local
        client.status = ClientStatus.processed
        client.priority = priority
        self.client_repository.update_client_status(client.id, ClientStatus.processed)

        return {
            "message": "Cliente processado com sucesso",
            "cliente_email": client.email,
            "status": ClientStatus.processed.value,
            "prioridade": priority.value,
        }