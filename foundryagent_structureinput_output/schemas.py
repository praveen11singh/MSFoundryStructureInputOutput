from typing import Optional

from pydantic import BaseModel


class OrderInfo(BaseModel):
    """Structured order details extracted from a customer request."""
    customer_name: str
    product: str
    quantity: int
    unit_price_usd: float
    total_usd: float
    priority: Optional[str] = None


def to_strict_json_schema(model: type[BaseModel]) -> dict:
    """Convert a Pydantic model into the strict JSON Schema shape the Responses API requires."""
    schema = model.model_json_schema()
    schema["additionalProperties"] = False
    schema["required"] = list(schema.get("properties", {}).keys())
    return schema
