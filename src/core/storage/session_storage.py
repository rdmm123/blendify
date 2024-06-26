from typing import Any
from flask import session

from src.core.storage.base import Storage


class SessionStorage(Storage):
    def write(self, to: str, value: Any, **params: Any) -> None:
        session[to] = value

    def read(self, source: str, **params: Any) -> Any:
        return session[source]

    def delete(self, where: str, **params: Any) -> None:
        try:
            del session[where]
        except KeyError:
            pass

    def flush(self, **params: Any) -> None:
        session.clear()
