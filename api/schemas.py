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


class ItemVendaRequest(StrictSchema):
    codigo: int
    quantidade: int


class VendaRequest(StrictSchema):
    itens: list[ItemVendaRequest]


class ItemVendaResponse(BaseModel):
    codigo: int
    quantidade: int
    subtotal: float
    estoque: int


class VendaResponse(BaseModel):
    total: float
    itens: list[ItemVendaResponse]