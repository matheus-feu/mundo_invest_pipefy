from app.infrastructure.integrations.pipefy.graphql_client import PipefyGraphQLClient
from app.schemas.client import ClientCreate


class ClientService:
	def __init__(self, repository, graphql_client: PipefyGraphQLClient):
		self.repository = repository
		self.graphql_client = graphql_client

	def create_card_payload(self, input_data: dict) -> dict:
		return self.graphql_client.build_create_card_payload(input_data)

	def update_card_payload(self, card_id: str, priority) -> dict:
		return self.graphql_client.build_update_card_payload(card_id, priority)

	def create_client(self, client_data: ClientCreate):
		client = self.repository.create_client(client_data)
		return client
