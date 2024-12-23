"""
Remote control HTTP request handler.
"""

import io
import subprocess
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

    # pylint: disable-next=C0103
    def do_POST(self) -> None:
        """Handle POST requests."""
        if self.path == "/mute":
            self.send_response(200)  # 200: OK
            self.end_headers()
            subprocess.run(
                ["/usr/bin/pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"],
                check=True,
            )
        else:
            self.send_response(400)  # 400: Bad Request
            self.end_headers()
