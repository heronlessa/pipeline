# src/app.py
# SmartShop Cloud - Sistema principal


def calcular_preco(preco_base, desconto):
    if desconto < 0 or desconto > 100:
        raise ValueError("Desconto deve ser entre 0 e 100")
    return round(preco_base * (1 - desconto / 100), 2)


def calcular_frete(peso_kg, distancia_km):
    if peso_kg <= 0:
        raise ValueError("Peso deve ser maior que zero")
    taxa_base = 5.0
    taxa_peso = peso_kg * 1.5
    taxa_distancia = distancia_km * 0.05
    return round(taxa_base + taxa_peso + taxa_distancia, 2)


def validar_estoque(quantidade, estoque_disponivel):
    if quantidade <= 0:
        raise ValueError("Quantidade deve ser maior que zero")
    return quantidade <= estoque_disponivel


def calcular_total_pedido(itens):
    if not itens:
        raise ValueError("Pedido não pode ser vazio")
    return round(sum(item["preco"] * item["quantidade"] for item in itens), 2)
