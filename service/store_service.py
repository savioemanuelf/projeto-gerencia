from service.repository import ProdutoRepository


class LojaService:
    def __init__(self, repository: ProdutoRepository | None = None):
        self.repository = repository or ProdutoRepository()
