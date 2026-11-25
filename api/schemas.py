from pydantic import BaseModel, ConfigDict


class StrictSchema(BaseModel):
    model_config = ConfigDict(strict=True, allow_inf_nan=False)


class ProdutoCreateRequest(StrictSchema):
    codigo: int
    preco: float


class QuantidadeRequest(StrictSchema):
    quantidade: int


class ProdutoResponse(BaseModel):
    codigo: int
    preco: float
    estoque: int


class EstoqueResponse(BaseModel):
    codigo: int
    estoque: int
