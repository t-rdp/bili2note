from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from mipac.http import HTTPClient

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager

__all__ = ('AbstractManager',)


class AbstractManager(ABC):
    @abstractmethod
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        pass
