from pydantic import BaseModel, EmailStr


class PipefyWebhook(BaseModel):
	event_id: str
	card_id: str
	cliente_email: EmailStr
	timestamp: str
