# Mundo Invest Backend

API em Python (FastAPI) para gerenciamento de clientes e simulação de integração com o Pipefy via GraphQL.

## Stacks utilizadas

- Python 3.14+
- FastAPI
- SQLAlchemy
- SQLite
- Pytest
- FastAPI
- GraphQL

## Instalação

1. Clone o repositório:
   ```bash
   git clone 
    cd mundo-invest-backend
    ```

2. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate  # Windows
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. Inicie o servidor:
    ```bash
    uvicorn main:app --reload
    ```
2. Acesse a documentação interativa da API em `http://localhost:8000/api/v1/docs`.
3. Use os endpoints para criar, listar, atualizar e deletar clientes, bem como para simular a integração com o Pipefy.
4. Para rodar os testes:
    ```bash
    pytest -q
    ```

## Endpoints disponíveis:

1. Criar cliente: `POST /api/v1/clientes/`

Exemplo de request:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_nome": "João Silva",
    "cliente_email": "joao.silva@example.com",
    "tipo_solicitacao": "Atualização cadastral",
    "valor_patrimonio": 250000
  }'
```

Resposta:

```json
{
  "id": 1,
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "status": "Aguardando Análise"
}
```

2. Webhook de integração com Pipefy: `POST /api/v1/webhooks/pipefy/card-updated/`
Exemplo de request:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/webhooks/pipefy/card-updated \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt_123",
    "card_id": "card_456",
    "cliente_email": "joao.silva@example.com",
    "timestamp": "2026-05-18T12:00:00Z"
  }'
```

Resposta:

```json
{
  "message": "Cliente processado com sucesso",
  "cliente_email": "joao.silva@example.com",
  "status": "Processado",
  "prioridade": "Prioridade Alta"
}
```

Se o evento já tiver sido processado:

```json
{
  "message": "Evento já processado",
  "event_id": "evt_123"
}
```

## Visão geral do projeto

Na versão atual, a aplicação usa FastAPI com sqlite local, oque é suficiente para teste técnico e desenvolvimento. 
Já em produção, essa estrutura pode ser escalada na AWS separando as responsabilidades entre camada de API, 
processamento de webook e a persistência de dados.

O API Gateway ficaria responsável por expor os endpoints públicos da aplicação. Enquanto isso, o AWS Lambda processaria as requisições, realizando a lógica de negócio e integração com o Pipefy.
O lambda faria a validação do payload de entrada, executaria as regras de negócios, faria a leitura e escrita no 
banco de dados e também a montagem dos mutations GraphQL para integração com o Pipefy e também o tratamento de 
idempotência dos eventos, com os handlers no lambda garantindo que eventos duplicados sejam ignorados.

Acho que essa abordagem é boa por que, escala automaticamente, reduz custo em baixa demanda, o custo se aplicaria 
apenas ao processamento efetivo, evita manter servidores ociosos, atuando com serverless e fácil de manter e 
implementar com os microserviços desacoplados, onde cada um tem uma responsabilidade clara.

Na persistência de dados, o uso do DynamoDB como opção, seria interessante, um modelo simples de chave-valor, onde a chave primária poderia ser o email do cliente, garantindo unicidade e fácil consulta.

A outra opção é o RDS Postgres que seria mais indicado caso queira manter um modelo relacional, vantagens que as 
consultas são completas, facilidade para gerar relatórios e aplicar regras.

O webhook deve registrar o event_id recebido como chave única para garantir a idempotência, e o processamento pode 
ser desacoplado também no serviço AWS SQS se necessário.


