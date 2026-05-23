from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.services.client_service import ClientService
from app.infrastructure.database.repositories.sql_client_repository import SQLClientRepository
from app.infrastructure.integrations.pipefy.graphql_client import PipefyGraphQLClient
from app.schemas.client import ClientCreate, ClientResponse

clients_router = APIRouter()


def get_client_service(db: Session = Depends(get_db)) -> ClientService:
	repository = SQLClientRepository(db)
	graphql_client = PipefyGraphQLClient()
	return ClientService(repository, graphql_client)


@clients_router.post("/clientes", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
		payload: ClientCreate,
		service: ClientService = Depends(get_client_service),
):
	try:
		return service.create_client(payload)
	except IntegrityError:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="Cliente com esse e-mail já existe.",
		)
