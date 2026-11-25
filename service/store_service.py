from decimal import Decimal

from service.exceptions import InvalidDataError, ProdutoAlreadyExistsError
from service.models import Produto
from service.repository import ProdutoRepository


class LojaService:
    def __init__(self, repository: ProdutoRepository | None = None):
        self.repository = repository or ProdutoRepository()

    def create_produto(self, codigo: int, preco: Decimal | int | float) -> Produto:
        self._validate_codigo(codigo)
        preco = self._parse_preco(preco)

        if self.repository.exists(codigo):
            raise ProdutoAlreadyExistsError(codigo)

        produto = Produto(codigo=codigo, preco=preco, estoque=0)
        self.repository.save(produto)
        return produto

    @staticmethod
    def _validate_codigo(codigo: int) -> None:
        if not isinstance(codigo, int) or isinstance(codigo, bool):
            raise InvalidDataError("Código deve ser um número inteiro")

    @staticmethod
    def _parse_preco(preco: Decimal | int | float) -> Decimal:
        if not isinstance(preco, (Decimal, int, float)) or isinstance(preco, bool):
            raise InvalidDataError("Preço deve ser um número")
        preco = Decimal(str(preco))
        if not preco.is_finite() or preco <= 0:
            raise InvalidDataError("Preço deve ser maior que zero")
        return preco
