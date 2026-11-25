from service.models import Produto


class ProdutoRepository:
    def __init__(self):
        self._produtos: dict[int, Produto] = {}

    def get(self, codigo: int) -> Produto | None:
        return self._produtos.get(codigo)

    def exists(self, codigo: int) -> bool:
        return codigo in self._produtos

    def save(self, produto: Produto) -> None:
        self._produtos[produto.codigo] = produto
