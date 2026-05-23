from abc import ABC, abstractmethod


class ClientRepository(ABC):

	@abstractmethod
	def create_client(self, client_data):
		pass

	@abstractmethod
	def get_client_by_email(self, email):
		pass

	@abstractmethod
	def update_client_status(self, client_id, status):
		pass

	@abstractmethod
	def get_client_by_id(self, client_id):
		pass
