from pydantic import BaseModel, ConfigDict


class StrictSchema(BaseModel):
    model_config = ConfigDict(strict=True, allow_inf_nan=False)


class ProdutoCreateRequest(StrictSchema):
    codigo: int
    preco: float


class ProdutoResponse(BaseModel):
    codigo: int
    preco: float
    estoque: int
