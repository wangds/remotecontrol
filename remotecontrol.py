#!/usr/bin/env python3

"""
Remote control web server main.
"""

from http.server import HTTPServer
from typing import Tuple

from src.remote_control_handler import RemoteControlHandler

SERVER_ADDRESS = ("", 8080)


def main() -> None:
    """Create RemoteControlHandler and serve forever."""
    webserver = HTTPServer(SERVER_ADDRESS, RemoteControlHandler)
    address: Tuple = webserver.server_address
    print(f"Server started http://{address[0]}:{address[1]}")

    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        pass

    webserver.server_close()
    print("Server stopped.")


if __name__ == "__main__":
    main()
