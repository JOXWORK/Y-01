import sys

import httpx


def main():
    try:
        response = httpx.get("http://127.0.0.1:8000/api/v1/service/healthcheck", timeout=5)

        if response.status_code == 204:
            sys.exit(0)

        raise Exception
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()
