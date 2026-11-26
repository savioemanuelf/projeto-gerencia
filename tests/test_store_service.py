import unittest
from decimal import Decimal

from service import LojaService
from service.exceptions import ProdutoAlreadyExistsError, ProdutoNotFoundError


class LojaServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.service = LojaService()


class TestCadastrarProduto(LojaServiceTestCase):
    def test_create_produto_com_codigo_preco_e_estoque_zero(self):
        produto = self.service.create_produto(123, Decimal("59.90"))

        self.assertEqual(produto.codigo, 123)
        self.assertEqual(produto.preco, Decimal("59.90"))
        self.assertEqual(produto.estoque, 0)
        self.assertEqual(self.service.get_estoque(123), 0)

    def test_create_produto_rejeita_codigo_ja_cadastrado(self):
        self.service.create_produto(123, Decimal("59.90"))

        with self.assertRaises(ProdutoAlreadyExistsError):
            self.service.create_produto(123, Decimal("10.00"))


if __name__ == "__main__":
    unittest.main()