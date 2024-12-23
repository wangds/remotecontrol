"""
State object.
"""

import json
import subprocess
from dataclasses import asdict, dataclass
from typing import Optional, Self


@dataclass
class State:
    """
    State object.
    """

    is_muted: Optional[bool] = None

    def json(self) -> str:
        """Return state as a JSON string."""
        return json.dumps(asdict(self))

    def populate_is_muted(self) -> Self:
        """Set `self.is_muted` to match audio mute state."""
        result = subprocess.run(
            ["/usr/bin/pactl", "get-sink-mute", "@DEFAULT_SINK@"],
            check=True,
            stdout=subprocess.PIPE,
            text=True,
        )
        self.is_muted = result.stdout.startswith("Mute: yes")
        return self
