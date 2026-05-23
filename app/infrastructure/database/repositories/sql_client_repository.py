from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError

from app.infrastructure.database.models.client import Client, ClientStatus, ClientPriority


class SQLClientRepository:
	def __init__(self, session):
		self.session = session

	def create_client(self, client_data):
		now = datetime.now(timezone.utc).isoformat()
		new_client = Client(
			name=client_data.cliente_nome,
			email=client_data.cliente_email,
			application_type=client_data.tipo_solicitacao,
			equity_value=client_data.valor_patrimonio,
			status=ClientStatus.awaiting_analysis,
			priority=ClientPriority.normal,
			created_at=now,
			updated_at=now,
		)
		self.session.add(new_client)
		try:
			self.session.commit()
			self.session.refresh(new_client)
			return new_client
		except IntegrityError:
			self.session.rollback()
			raise

	def get_client_by_email(self, email: str):
		return self.session.query(Client).filter_by(email=email).first()

	def update_client_status(self, client_id: int, status: ClientStatus):
		client = self.session.query(Client).filter_by(id=client_id).first()
		if not client:
			return None
		client.status = status
		try:
			self.session.commit()
			self.session.refresh(client)
			return client
		except IntegrityError:
			self.session.rollback()
			raise

	def update_client_processing(self, client_id: int, status: ClientStatus, priority: ClientPriority):
		client = self.session.query(Client).filter_by(id=client_id).first()
		if not client:
			return None
		client.status = status
		client.priority = priority
		try:
			self.session.commit()
			self.session.refresh(client)
			return client
		except IntegrityError:
			self.session.rollback()
			raise

	def get_client_by_id(self, client_id: int):
		return self.session.query(Client).filter_by(id=client_id).first()
