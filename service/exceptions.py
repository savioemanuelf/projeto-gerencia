class DomainError(Exception):
    """Base para todos os erros de regra de negócio"""


class InvalidDataError(DomainError):
    """Dados invalidos para a operação"""


class ProdutoNotFoundError(DomainError):
    """O produto informado não existe"""

    def __init__(self, codigo: int):
        self.codigo = codigo
        super().__init__(f"Produto {codigo} não encontrado")


class ProdutoAlreadyExistsError(DomainError):
    """Já existe um produto com o código informado"""

    def __init__(self, codigo: int):
        self.codigo = codigo
        super().__init__(f"Produto {codigo} já cadastrado")
