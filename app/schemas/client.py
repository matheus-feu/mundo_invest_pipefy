from pydantic import BaseModel, EmailStr, ConfigDict


class ClientCreate(BaseModel):
	cliente_nome: str
	cliente_email: EmailStr
	tipo_solicitacao: str
	valor_patrimonio: float


class ClientResponse(BaseModel):
	id: int
	name: str
	email: str
	status: str

	model_config = ConfigDict(from_attributes=True)
