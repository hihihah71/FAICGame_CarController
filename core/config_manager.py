from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


DEFAULT_CONFIG: dict[str, Any] = {
    "camera": {
        "index": 0,
        "width": 640,
        "height": 480,
    },
    "racing": {
        "steer_threshold": 15,
        "drift_steer_threshold": 5,
        "boost_zone_ratio": 0.25,
        "drift_zone_ratio": 0.70,
    },
    "keys": {
        "forward": "w",
        "left": "a",
        "right": "d",
        "drift": "s",
        "boost": "space",
    },
    "hud": {
        "theme": "neon",
        "show_fps": True,
        "show_landmarks": True,
    },
}


class ConfigManager:
    def __init__(self, path: str | Path = "config.json") -> None:
        self.path = Path(path)

    def ensure_exists(self) -> dict[str, Any]:
        if not self.path.exists():
            self.save(copy.deepcopy(DEFAULT_CONFIG))
        return self.load()

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return self.ensure_exists()

        with self.path.open("r", encoding="utf-8") as file:
            loaded = json.load(file)
        return self._merge_defaults(copy.deepcopy(DEFAULT_CONFIG), loaded)

    def save(self, config: dict[str, Any]) -> None:
        self.path.write_text(
            json.dumps(config, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def reset_default(self) -> dict[str, Any]:
        config = copy.deepcopy(DEFAULT_CONFIG)
        self.save(config)
        return config

    def _merge_defaults(self, default: dict[str, Any], loaded: dict[str, Any]) -> dict[str, Any]:
        for key, value in loaded.items():
            if isinstance(value, dict) and isinstance(default.get(key), dict):
                default[key] = self._merge_defaults(default[key], value)
            else:
                default[key] = value
        return default
