import json
from contextlib import asynccontextmanager
from typing import Any, Dict

import requests
from fastapi import FastAPI, status
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

from src.payment import PaymentPixRequest, GatewayPayment, PaymentPixResponse
from src.repository import Repository
from src.settings import Settings

settings = Settings()
engine = create_engine(settings.DATABASE_URL, echo=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    with Session(engine) as session:
        SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


class HealthCheck(BaseModel):
    status: str = "OK"


class ResponseInput(BaseModel):
    amount: int
    caller_id: int
    client_id: int
    created_at: str
    id: str
    payment: Dict[str, Any]
    state: str
    additional_info: Dict[str, Any]


@app.get(
    "/",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    return HealthCheck(status="OK")


@app.post(
    "/payment",
    response_model=PaymentPixResponse,
)
def create_payment(data: PaymentPixRequest):
    repo = Repository(engine=engine)
    mercadopago = GatewayPayment(repository=repo, settings=settings)

    payment = mercadopago.create_payment(data=data)
    print(payment)
    return payment


@app.post("/notification/{transaction_id}")
def create_notification(transaction_id: str, data: dict):

    url = settings.BOT_URL
    headers = {
        "Authorization": f'Bearer {settings.BOT_API_TOKEN}',
        "Content-Type": "application/json"
    }
    body = {
        "transaction_id": transaction_id
    }

    response = requests.post(url, headers=headers, json=body)
    print(response)
    # data_dict = data.model_dump()

    # repo = Repository(engine=engine)
    # repo.create_response(data=data_dict)
    print(data)
    return
