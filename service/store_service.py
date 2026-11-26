from decimal import Decimal

from service.exceptions import (
    InvalidDataError,
    ProdutoAlreadyExistsError,
    ProdutoNotFoundError,
)
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

    def get_estoque(self, codigo: int) -> int:
        return self._get_produto(codigo).estoque

    def add_estoque(self, codigo: int, quantidade: int) -> int:
        self._validate_quantidade(quantidade)
        produto = self._get_produto(codigo)
        produto.estoque += quantidade
        self.repository.save(produto)
        return produto.estoque

    def remove_estoque(self, codigo: int, quantidade: int) -> int:
        self._validate_quantidade(quantidade)
        produto = self._get_produto(codigo)
        if quantidade > produto.estoque:
            raise InvalidDataError("Estoque insuficiente")
        produto.estoque -= quantidade
        self.repository.save(produto)
        return produto.estoque

    def create_venda(self, itens: list[tuple[int, int]]) -> dict:
        if not itens:
            raise InvalidDataError("A venda deve ter pelo menos um item")

        produtos = {}
        total_por_codigo = {}
        for codigo, quantidade in itens:
            self._validate_quantidade(quantidade)
            produtos[codigo] = self._get_produto(codigo)
            total_por_codigo[codigo] = total_por_codigo.get(codigo, 0) + quantidade

        for codigo, quantidade_total in total_por_codigo.items():
            if quantidade_total > produtos[codigo].estoque:
                raise InvalidDataError(f"Estoque insuficiente para o produto {codigo}")

        resultado = []
        total = Decimal("0")
        for codigo, quantidade in itens:
            produto = produtos[codigo]
            produto.estoque -= quantidade
            self.repository.save(produto)
            subtotal = produto.preco * quantidade
            total += subtotal
            resultado.append(
                {
                    "codigo": codigo,
                    "quantidade": quantidade,
                    "subtotal": subtotal,
                    "estoque": produto.estoque,
                }
            )

        return {"total": total, "itens": resultado}

    def _get_produto(self, codigo: int) -> Produto:
        self._validate_codigo(codigo)
        produto = self.repository.get(codigo)
        if produto is None:
            raise ProdutoNotFoundError(codigo)
        return produto

    @staticmethod
    def _validate_codigo(codigo: int) -> None:
        if not isinstance(codigo, int) or isinstance(codigo, bool):
            raise InvalidDataError("Código deve ser um número inteiro")

    @staticmethod
    def _validate_quantidade(quantidade: int) -> None:
        if not isinstance(quantidade, int) or isinstance(quantidade, bool):
            raise InvalidDataError("Quantidade deve ser um número inteiro")
        if quantidade <= 0:
            raise InvalidDataError("Quantidade deve ser maior que zero")

    @staticmethod
    def _parse_preco(preco: Decimal | int | float) -> Decimal:
        if not isinstance(preco, (Decimal, int, float)) or isinstance(preco, bool):
            raise InvalidDataError("Preço deve ser um número")
        preco = Decimal(str(preco))
        if not preco.is_finite() or preco <= 0:
            raise InvalidDataError("Preço deve ser maior que zero")
        return preco
