# Loja - Controle de Produtos e Estoque

Sistema básico de e-commerce para controle de produtos e estoque de uma loja
virtual, desenvolvido para a disciplina de Gerência de Configuração.

## Arquitetura (3 camadas)

```
service/   Camada de serviço (regras de negócio). Não depende de FastAPI.
api/       API REST (FastAPI). Apenas repassa as requisições para o serviço.
cli/       Front-end em console. Consome a API REST via httpx.
```

Os dados ficam apenas em memória (sem banco de dados)

## Como executar

Requer Python 3.10+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

API (em um terminal):

```bash
uvicorn api.main:app --reload
```

Documentação interativa: http://127.0.0.1:8000/docs

Front-end (em outro terminal):

```bash
python -m cli.main
```
## Testes

Testes unitários da camada de serviço. Na raiz do projeto, com o ambiente
virtual ativo:

```bash
python -m unittest discover -s tests -t . -v
```
