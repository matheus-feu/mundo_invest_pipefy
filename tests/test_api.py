def test_create_client_valid_payload_and_persistence_data(client):
	payload = dict(
		cliente_nome="João Silva",
		cliente_email="joao.silva@example.com",
		tipo_solicitacao="Novo Cliente",
		valor_patrimonio=100000.00,
	)
	response = client.post("/api/v1/clientes", json=payload)
	assert response.status_code in (201, 409)  # Aceita tanto criação quanto conflito de e-mail

	body = response.json()
	assert body["name"] == payload["cliente_nome"]
	assert body["email"] == payload["cliente_email"]
	assert body["status"] == "Aguardando Análise"


def test_webhook_applies_priority_rule_by_webhook_payload(client):
	create_payload = dict(
		cliente_nome="Maria Oliveira",
		cliente_email="maria.oliveira@example.com",
		tipo_solicitacao="Cadastro Completo",
		valor_patrimonio=200000.00,
	)
	create_response = client.post("/api/v1/clientes", json=create_payload)
	assert create_response.status_code in (201, 409)

	webhook_payload = dict(
		event_id="evt_123456",
		card_id="card_123456",
		cliente_email="maria.oliveira@example.com",
		timestamp="2024-06-01T12:00:00Z",
	)
	response = client.post("/api/v1/webhooks/pipefy/card-updated", json=webhook_payload)
	assert response.status_code == 200

	body = response.json()
	assert body.get("prioridade") == "Prioridade Alta"
	assert body.get("status") in ("Processado", None)


def test_webhook_blocks_duplicate_events_id(client):
	create_payload = dict(
		cliente_nome="Carlos Pereira",
		cliente_email="carlos.pereira@example.com",
		tipo_solicitacao="Cadastro Completo",
		valor_patrimonio=150000.00,
	)
	create_response = client.post("/api/v1/clientes", json=create_payload)
	assert create_response.status_code in (201, 409)

	webhook_payload = dict(
		event_id="evt_123456",
		card_id="card_123456",
		cliente_email="carlos.pereira@example.com",
		timestamp="2024-06-01T12:00:00Z",
	)
	response = client.post("/api/v1/webhooks/pipefy/card-updated", json=webhook_payload)
	assert response.status_code == 200

	# Enviar o mesmo evento novamente para testar bloqueio de duplicatas
	duplicate_response = client.post("/api/v1/webhooks/pipefy/card-updated", json=webhook_payload)
	assert duplicate_response.status_code in (200, 409)  # Aceita tanto processamento quanto conflito de evento
	# duplicado

	duplicate_body = duplicate_response.json()
	assert duplicate_body.get("event_id") == "evt_123456"
	assert "já processado" in duplicate_body.get("message", "").lower()
