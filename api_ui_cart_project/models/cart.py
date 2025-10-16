
from pydantic import BaseModel
from typing import Optional

class AddToCartResponse(BaseModel):
    success: bool
    message: str
    updatetopcartsectionhtml: str
    updateflyoutcartsectionhtml: Optional[str] = None


class AddToCartRequest(BaseModel):
    product_id: int
    qty: int = 1

    def as_form(self) -> dict:
        return {f"addtocart_{self.product_id}.EnteredQuantity": str(self.qty)}
