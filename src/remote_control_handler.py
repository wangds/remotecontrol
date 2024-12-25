"""
Remote control HTTP request handler.
"""

import io
import subprocess
from http.server import BaseHTTPRequestHandler

from src.state import State


class RemoteControlHandler(BaseHTTPRequestHandler):
    """Remote control HTTP request handler."""

    # pylint: disable-next=C0103
    def do_GET(self) -> None:
        """Handle GET requests."""
        content_type = "text/html; charset=utf-8"

        if self.path == "/favicon.svg":
            src = io.FileIO(self.path[1:]).read()
            content_type = "image/svg+xml"
        elif self.path == "/index.css":
            src = io.FileIO(self.path[1:]).read()
        else:
            src = self.render_index()

        self.send_response(200)  # 200: OK
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(src)

    def render_index(self) -> bytes:
        """Render index.html."""
        with open("index.html", encoding="utf-8") as f:
            state = State().populate_is_muted()
            template = f.read()
            template = template.replace("{{ STATE }}", state.json())
            return bytes(template, "utf-8")

    # pylint: disable-next=C0103
    def do_POST(self) -> None:
        """Handle POST requests."""
        if self.path == "/mute":
            self.send_response(200)  # 200: OK
            self.send_header("Content-type", "text/json")
            self.end_headers()
            subprocess.run(
                ["/usr/bin/pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"],
                check=True,
            )

            state = State().populate_is_muted()
            self.wfile.write(bytes(state.json(), "utf-8"))
        elif self.path == "/volDown" or self.path == "/volUp":
            self.send_response(200)  # 200: OK
            self.send_header("Content-type", "text/json")
            self.end_headers()
            adjust = "-5%" if self.path == "/volDown" else "+5%"
            subprocess.run(
                ["/usr/bin/pactl", "set-sink-volume", "@DEFAULT_SINK@", adjust],
                check=True,
            )
        else:
            self.send_response(400)  # 400: Bad Request
            self.end_headers()
