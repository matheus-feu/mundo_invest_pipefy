from enum import Enum

from sqlalchemy import Column, Integer, String, Float, Enum as SqlEnum

from app.core.database import Base


class ClientStatus(str, Enum):
	awaiting_analysis = "Aguardando Análise"
	processed = "Processado"


class ClientPriority(str, Enum):
	high = "Prioridade Alta"
	normal = "Prioridade Normal"


class Client(Base):
	__tablename__ = "clients"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, index=True)
	email = Column(String, unique=True, index=True)
	application_type = Column(String, nullable=False)
	equity_value = Column(Float, nullable=False)
	status = Column(
		SqlEnum(ClientStatus, name="client_status"),
		default=ClientStatus.awaiting_analysis,
		nullable=False,
	)
	priority = Column(
		SqlEnum(ClientPriority, name="client_priority"),
		default=ClientPriority.normal,
		nullable=False,
	)
	created_at = Column(String, nullable=False)
	updated_at = Column(String, nullable=False)