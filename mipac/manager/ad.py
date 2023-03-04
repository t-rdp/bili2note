from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.manager import AbstractManager
from mipac.http import HTTPClient, Route

if TYPE_CHECKING:
    from mipac.client import ClientManager

__all__ = ('AdminAdvertisingManager',)


class AdminAdvertisingManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientManager):
        self.__session: HTTPClient = session
        self.__client: ClientManager = client

    async def create(
        self,
        url: str,
        memo: str,
        place: str,
        priority: str,
        ratio: str,
        expires_at: int,
        image_url: str,
    ):
        data = {
            'url': url,
            'memo': memo,
            'place': place,
            'priority': priority,
            'ratio': ratio,
            'expires_at': expires_at,
            'image_url': image_url,
        }
        return await self.__session.request(
            Route('POST', '/api/admin/ad/create'),
            json=data,
            auth=True,
            lower=True,
        )
