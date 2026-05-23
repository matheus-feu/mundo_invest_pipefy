from sqlalchemy import Column, Integer, String

from app.core.database import Base


class WebhookEvent(Base):
	__tablename__ = "webhook_events"

	id = Column(Integer, primary_key=True, index=True)
	event_id = Column(String, unique=True)
	card_id = Column(String)
	client_email = Column(String)
	timestamp = Column(String)
	processed_at = Column(String, nullable=True)
