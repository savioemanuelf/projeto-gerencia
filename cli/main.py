import httpx

API_URL = "http://127.0.0.1:8000"


def _exibir_resposta(response: httpx.Response) -> None:
    try:
        dados = response.json()
    except ValueError:
        print(f"[{response.status_code}] {response.text}")
        return

    if response.is_error and isinstance(dados, dict) and "erro" in dados:
        print(f"Erro ({response.status_code}): {dados['erro']}")
    else:
        print(f"Sucesso ({response.status_code}): {dados}")


def cadastrar_produto(client: httpx.Client) -> None:
    try:
        codigo = int(input("Código do produto: ").strip())
        preco = float(input("Preço do produto: ").strip())
    except ValueError:
        print("Erro: código deve ser inteiro e preço deve ser numérico.")
        return

    response = client.post("/loja/produto", json={"codigo": codigo, "preco": preco})
    _exibir_resposta(response)


def consultar_estoque(client: httpx.Client) -> None:
    try:
        codigo = int(input("Código do produto: ").strip())
    except ValueError:
        print("Erro: código deve ser um número inteiro.")
        return

    response = client.get(f"/loja/produto/{codigo}/estoque")
    _exibir_resposta(response)


def entrada_estoque(client: httpx.Client) -> None:
    try:
        codigo = int(input("Código do produto: ").strip())
        quantidade = int(input("Quantidade de entrada: ").strip())
    except ValueError:
        print("Erro: código e quantidade devem ser números inteiros.")
        return

    response = client.put(f"/loja/produto/{codigo}/entrada", json={"quantidade": quantidade})
    _exibir_resposta(response)


def saida_estoque(client: httpx.Client) -> None:
    try:
        codigo = int(input("Código do produto: ").strip())
        quantidade = int(input("Quantidade de saída: ").strip())
    except ValueError:
        print("Erro: código e quantidade devem ser números inteiros.")
        return

    response = client.put(f"/loja/produto/{codigo}/saida", json={"quantidade": quantidade})
    _exibir_resposta(response)


def realizar_venda(client: httpx.Client) -> None:
    itens = []
    print("Informe os itens da venda (deixe o código em branco e pressione Enter para finalizar):")

    while True:
        codigo_str = input("  Código do produto: ").strip()
        if codigo_str == "":
            break

        quantidade_str = input("  Quantidade: ").strip()
        try:
            codigo = int(codigo_str)
            quantidade = int(quantidade_str)
        except ValueError:
            print("  Erro: código e quantidade devem ser números inteiros. Item ignorado.")
            continue

        itens.append({"codigo": codigo, "quantidade": quantidade})

    response = client.post("/loja/venda", json={"itens": itens})
    _exibir_resposta(response)


def main() -> None:
    with httpx.Client(base_url=API_URL, timeout=10.0) as client:
        while True:
            print("\n=== Loja - Controle de Produtos e Estoque ===")
            print("1 - Cadastrar Produto")
            print("2 - Consultar Estoque")
            print("3 - Entrada de Estoque")
            print("4 - Saída de Estoque")
            print("5 - Realizar Venda")
            print("0 - Sair")

            opcao = input("> ").strip()

            try:
                if opcao == "1":
                    cadastrar_produto(client)
                elif opcao == "2":
                    consultar_estoque(client)
                elif opcao == "3":
                    entrada_estoque(client)
                elif opcao == "4":
                    saida_estoque(client)
                elif opcao == "5":
                    realizar_venda(client)
                elif opcao == "0":
                    print("Obrigado por visitar a nossa loja!")
                    break
                else:
                    print("Opção inválida.")
            except httpx.ConnectError:
                print(
                    "Erro: não foi possível conectar à API em http://127.0.0.1:8000. "
                    "Verifique se o servidor está rodando."
                )


if __name__ == "__main__":
    main()
