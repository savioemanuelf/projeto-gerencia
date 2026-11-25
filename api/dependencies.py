from service import LojaService

_loja_service = LojaService()


def get_loja_service() -> LojaService:
    return _loja_service
