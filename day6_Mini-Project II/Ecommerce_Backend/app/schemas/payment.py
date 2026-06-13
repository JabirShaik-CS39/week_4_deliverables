from pydantic import BaseModel


class PaymentRequest(BaseModel):
    order_id: int


class PaymentResponse(BaseModel):
    message: str
    order_id: int
    status: str