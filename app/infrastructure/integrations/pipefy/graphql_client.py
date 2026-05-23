from app.core.config import settings
from app.infrastructure.integrations.pipefy.mutations import CREATE_CARD_MUTATION, UPDATE_CARD_MUTATION


class PipefyGraphQLClient:

	@staticmethod
	def build_create_card_payload(input_data: dict) -> dict:
		return {
			"query": CREATE_CARD_MUTATION,
			"variables": {
				"input": {
					"pipe_id": int(settings.pipefy_pipe_id),
					"title": f"{input_data['client_name']} - {input_data['client_email']}",
					"fields_attributes": [
						{"field_id": "cliente_nome", "field_value": input_data["client_name"]},
						{"field_id": "cliente_email", "field_value": input_data["client_email"]},
						{"field_id": "valor_patrimonio", "field_value": str(input_data["client_assets"])},
					],
				}
			},
		}

	@staticmethod
	def build_update_card_payload(card_id: str, priority: str) -> dict:
		return {
			"query": UPDATE_CARD_MUTATION,
			"variables": {
				"input": {
					"id": card_id,
					"fields_attributes": [
						{"field_id": "prioridade", "field_value": priority},
					],
				}
			},
		}
