from fastapi import APIRouter, Depends, status

from api.dependencies import get_loja_service
from api.schemas import (
    EstoqueResponse,
    ProdutoCreateRequest,
    ProdutoResponse,
    QuantidadeRequest,
)
from service import LojaService

router = APIRouter(prefix="/loja")


@router.post("/produto", status_code=status.HTTP_201_CREATED, response_model=ProdutoResponse)
def create_produto(
    request: ProdutoCreateRequest,
    service: LojaService = Depends(get_loja_service),
):
    produto = service.create_produto(request.codigo, request.preco)
    return ProdutoResponse(codigo=produto.codigo, preco=float(produto.preco), estoque=produto.estoque)


@router.get("/produto/{codigo}/estoque", response_model=EstoqueResponse)
def get_estoque(codigo: int, service: LojaService = Depends(get_loja_service)):
    estoque = service.get_estoque(codigo)
    return EstoqueResponse(codigo=codigo, estoque=estoque)


@router.put("/produto/{codigo}/entrada", response_model=EstoqueResponse)
def add_estoque(
    codigo: int,
    request: QuantidadeRequest,
    service: LojaService = Depends(get_loja_service),
):
    estoque = service.add_estoque(codigo, request.quantidade)
    return EstoqueResponse(codigo=codigo, estoque=estoque)


@router.put("/produto/{codigo}/saida", response_model=EstoqueResponse)
def remove_estoque(
    codigo: int,
    request: QuantidadeRequest,
    service: LojaService = Depends(get_loja_service),
):
    estoque = service.remove_estoque(codigo, request.quantidade)
    return EstoqueResponse(codigo=codigo, estoque=estoque)