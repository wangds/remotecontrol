"""
Remote control HTTP request handler.
"""

import io
from http.server import BaseHTTPRequestHandler


class RemoteControlHandler(BaseHTTPRequestHandler):
    """Remote control HTTP request handler."""

    # pylint: disable-next=C0103
    def do_GET(self) -> None:
        """Handle GET requests."""
        self.send_response(200)  # 200: OK
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(io.FileIO("index.html").read())
