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


class TestConsultarEstoque(LojaServiceTestCase):
    def test_get_estoque_retorna_estoque_correto(self):
        self.service.create_produto(123, Decimal("59.90"))
        self.service.add_estoque(123, 15)

        self.assertEqual(self.service.get_estoque(123), 15)

    def test_get_estoque_produto_inexistente(self):
        with self.assertRaises(ProdutoNotFoundError):
            self.service.get_estoque(999)


class TestEntradaEstoque(LojaServiceTestCase):
    def test_add_estoque_soma_quantidade(self):
        self.service.create_produto(123, Decimal("59.90"))

        self.assertEqual(self.service.add_estoque(123, 10), 10)
        self.assertEqual(self.service.add_estoque(123, 5), 15)
        self.assertEqual(self.service.get_estoque(123), 15)

    def test_add_estoque_produto_inexistente(self):
        with self.assertRaises(ProdutoNotFoundError):
            self.service.add_estoque(999, 10)


class TestSaidaEstoque(LojaServiceTestCase):
    def test_remove_estoque_subtrai_quantidade(self):
        self.service.create_produto(123, Decimal("59.90"))
        self.service.add_estoque(123, 10)

        self.assertEqual(self.service.remove_estoque(123, 4), 6)
        self.assertEqual(self.service.get_estoque(123), 6)

    def test_remove_estoque_produto_inexistente(self):
        with self.assertRaises(ProdutoNotFoundError):
            self.service.remove_estoque(999, 1)

    def test_remove_estoque_maior_que_estoque_deixa_negativo(self):
        self.service.create_produto(123, Decimal("59.90"))
        self.service.add_estoque(123, 5)

        self.assertEqual(self.service.remove_estoque(123, 8), -3)
        self.assertEqual(self.service.get_estoque(123), -3)


if __name__ == "__main__":
    unittest.main()