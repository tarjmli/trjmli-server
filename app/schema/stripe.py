from pydantic import BaseModel
from decimal import Decimal

class PaymentBase(BaseModel):
    amount: Decimal

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int
    status: str
    stripe_session_id: str

    class Config:
        from_attributes = True
