from fastapi import APIRouter, Depends, status

from api.dependencies import get_loja_service
from api.schemas import ProdutoCreateRequest, ProdutoResponse
from service import LojaService

router = APIRouter(prefix="/loja")


@router.post("/produto", status_code=status.HTTP_201_CREATED, response_model=ProdutoResponse)
def create_produto(
    request: ProdutoCreateRequest,
    service: LojaService = Depends(get_loja_service),
):
    produto = service.create_produto(request.codigo, request.preco)
    return ProdutoResponse(codigo=produto.codigo, preco=float(produto.preco), estoque=produto.estoque)
