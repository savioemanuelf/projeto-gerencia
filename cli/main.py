import os

import httpx

API_URL = os.environ.get("LOJA_API_URL", "http://127.0.0.1:8000")


def main():
    with httpx.Client(base_url=API_URL, timeout=10) as client:
        print(f"Loja - cliente de console (API: {client.base_url})")
        # TODO: Implementar menu


if __name__ == "__main__":
    main()
