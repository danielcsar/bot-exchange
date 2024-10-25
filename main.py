import mercadopago
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class HealthCheck(BaseModel):
    status: str = "OK"


@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    return HealthCheck(status="OK")


@app.post("/payment")
def create_payment():
    sdk = mercadopago.SDK("PROD_ACCESS_TOKEN")

    # Cria um item na preferência
    preference_data = {
        "items": [
            {
                "id": 1,
                "title": "BTC",
                "quantity": 1,
                "unit_price": 100
            }
        ],
        "payment_method_id": "Pix",
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]

    return {"Hello": preference}
