# tests/test_app.py
import pytest
from src.app import calcular_preco, calcular_frete, validar_estoque, calcular_total_pedido


class TestCalcularPreco:
    def test_sem_desconto(self):
        assert calcular_preco(100.0, 0) == 100.0

    def test_desconto_50(self):
        assert calcular_preco(200.0, 50) == 100.0

    def test_desconto_100(self):
        assert calcular_preco(100.0, 100) == 0.0

    def test_desconto_invalido_negativo(self):
        with pytest.raises(ValueError):
            calcular_preco(100.0, -10)

    def test_desconto_invalido_acima_100(self):
        with pytest.raises(ValueError):
            calcular_preco(100.0, 110)


class TestCalcularFrete:
    def test_frete_basico(self):
        assert calcular_frete(1.0, 10) == 7.0

    def test_frete_peso_zero(self):
        with pytest.raises(ValueError):
            calcular_frete(0, 10)

    def test_frete_peso_grande(self):
        assert calcular_frete(10.0, 100) == 25.0


class TestValidarEstoque:
    def test_estoque_suficiente(self):
        assert validar_estoque(5, 10) is True

    def test_estoque_insuficiente(self):
        assert validar_estoque(15, 10) is False

    def test_estoque_exato(self):
        assert validar_estoque(10, 10) is True

    def test_quantidade_invalida(self):
        with pytest.raises(ValueError):
            validar_estoque(0, 10)


class TestCalcularTotalPedido:
    def test_pedido_simples(self):
        itens = [{"preco": 10.0, "quantidade": 2}]
        assert calcular_total_pedido(itens) == 20.0

    def test_pedido_multiplos_itens(self):
        itens = [
            {"preco": 10.0, "quantidade": 2},
            {"preco": 5.0,  "quantidade": 3},
        ]
        assert calcular_total_pedido(itens) == 35.0

    def test_pedido_vazio(self):
        with pytest.raises(ValueError):
            calcular_total_pedido([])
