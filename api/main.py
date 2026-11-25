from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.routes import router
from service import (
    InvalidDataError,
    ProdutoAlreadyExistsError,
    ProdutoNotFoundError,
)

app = FastAPI(title="Loja - Controle de Produtos e Estoque")
app.include_router(router)


@app.exception_handler(RequestValidationError)
async def handle_validation_error(request: Request, exc: RequestValidationError):
    # sobrescrevendo o 422 padrão do fastApi por 400 Bad Request
    return JSONResponse(status_code=400, content={"erro": "Requisição inválida"})


@app.exception_handler(InvalidDataError)
async def handle_invalid_data(request: Request, exc: InvalidDataError):
    return JSONResponse(status_code=400, content={"erro": str(exc)})


@app.exception_handler(ProdutoNotFoundError)
async def handle_produto_not_found(request: Request, exc: ProdutoNotFoundError):
    return JSONResponse(status_code=404, content={"erro": str(exc)})


@app.exception_handler(ProdutoAlreadyExistsError)
async def handle_produto_already_exists(request: Request, exc: ProdutoAlreadyExistsError):
    return JSONResponse(status_code=409, content={"erro": str(exc)})
