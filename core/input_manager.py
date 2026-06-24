from __future__ import annotations

from typing import Iterable

import keyinput


class InputManager:
    def __init__(self, key_mapping: dict[str, str]) -> None:
        self.key_mapping = key_mapping
        self._pressed: set[str] = set()

    def press(self, key: str) -> None:
        if key not in self._pressed:
            keyinput.press_key(key)
            self._pressed.add(key)

    def release(self, key: str) -> None:
        if key in self._pressed:
            keyinput.release_key(key)
            self._pressed.remove(key)

    def set_pressed_keys(self, keys: Iterable[str]) -> None:
        desired = set(keys)
        for key in list(self._pressed - desired):
            self.release(key)
        for key in desired - self._pressed:
            self.press(key)

    def release_all(self) -> None:
        for key in list(self._pressed):
            self.release(key)

    def get_pressed_keys(self) -> set[str]:
        return set(self._pressed)
