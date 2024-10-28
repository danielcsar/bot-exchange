import uuid

import mercadopago
from pydantic import BaseModel, field_validator
from src.settings import Settings


settings = Settings()

sdk = mercadopago.SDK(settings.ACCESS_TOKEN)


class PaymentPixRequest(BaseModel):
    amount_in_cents: float
    wallet_address: str

    @field_validator('amount_in_cents')
    @classmethod
    def cents(cls, v: int) -> float:
        return v / 100


class PaymentPixResponse(BaseModel):
    transaction_id: str
    pix_copy_paste: str
    qr_code: str
    link: str


class GatewayPayment:
    def __init__(self, repository):
        self.repository = repository

    def create_payment(self, *, data: PaymentPixRequest) -> PaymentPixResponse:
        user = self.repository.create_user(wallet_address=data.wallet_address)

        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {
            'x-idempotency-key': str(user.id_external)
        }

        payment_data = {
            "installments": 1,
            "transaction_amount": 0.01,
            "description": "BTC",
            "payment_method_id": 'pix',
            "payer": {
                "email": "user1@user.com.br"
            },
            "external_reference": str(user.id_external)
        }

        # if notification_url:
        #     payment_data['notification_url'] = notification_url

        result = sdk.payment().create(payment_data, request_options)

        response = PaymentPixResponse(
            transaction_id=str(user.id_external),
            pix_copy_paste=result['response']['point_of_interaction']['transaction_data']['qr_code'],
            qr_code=result['response']['point_of_interaction']['transaction_data']['qr_code_base64'],
            link=result['response']['point_of_interaction']['transaction_data']['ticket_url']
        )
        return response
