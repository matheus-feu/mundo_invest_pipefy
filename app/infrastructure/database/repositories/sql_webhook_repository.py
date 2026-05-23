from datetime import datetime

from sqlalchemy.exc import IntegrityError

from app.infrastructure.database.models.webhook_event import WebhookEvent


class SQLWebhookRepository:
	def __init__(self, session):
		self.session = session

	def exists(self, event_id: str) -> bool:
		return self.session.query(WebhookEvent).filter_by(event_id=event_id).first() is not None

	def create_webhook_event(
			self,
			event_id: str,
			card_id: str,
			client_email: str,
			timestamp: str,
	) -> WebhookEvent:
		webhook_event = WebhookEvent(
			event_id=event_id,
			card_id=card_id,
			client_email=client_email,
			timestamp=timestamp,
		)
		self.session.add(webhook_event)
		self.session.commit()
		self.session.refresh(webhook_event)
		return webhook_event

	def register_if_not_exists(
			self,
			event_id: str,
			card_id: str,
			client_email: str,
			timestamp: str,
	) -> bool:
		"""
		True  -> evento registrado agora (processar webhook)
		False -> evento duplicado (não processar novamente)
		"""
		webhook_event = WebhookEvent(
			event_id=event_id,
			card_id=card_id,
			client_email=client_email,
			timestamp=timestamp,
		)
		self.session.add(webhook_event)
		try:
			self.session.commit()
			return True
		except IntegrityError:
			self.session.rollback()
			return False
