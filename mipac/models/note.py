from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal, Optional

from mipac.errors.base import NotExistRequiredData
from mipac.models.lite.user import LiteUser
from mipac.models.poll import Poll
from mipac.types.note import (
    INoteState,
    INoteTranslateResult,
    INoteUpdated,
    INoteUpdatedDelete,
)
from mipac.util import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.manager.note import ClientNoteManager
    from mipac.models.user import UserDetailed
    from mipac.types.drive import IDriveFile
    from mipac.types.emoji import ICustomEmojiLite
    from mipac.types.note import INote, INoteReaction

__all__ = (
    'NoteState',
    'Note',
    'Follow',
    'Header',
    'NoteReaction',
    'NoteDeleted',
    'NoteTranslateResult',
)


class NoteState:
    def __init__(self, data: INoteState) -> None:
        self.__data: INoteState = data

    @property
    def is_favorite(self) -> bool:
        return self.__data['is_favorited']

    @property
    def is_watching(self) -> bool:
        return self.__data['is_watching']

    @property
    def is_muted_thread(self) -> bool:
        return self.__data.get('is_muted_thread', False)


class NoteDeleted:
    def __init__(self, data: INoteUpdated[INoteUpdatedDelete]) -> None:
        self.__data = data

    @property
    def note_id(self) -> str:
        return self.__data['body']['id']

    @property
    def deleted_at(self) -> datetime:
        return str_to_datetime(self.__data['body']['body']['deleted_at'])


class Follow:
    def __init__(self, data):
        self.id: str | None = data.get('id')
        self.created_at: Optional[datetime] = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        ) if data.get('created_at') else None
        self.type: str | None = data.get('type')
        self.user: Optional[UserDetailed] = data.get('user')

    async def follow(self) -> tuple[bool, str | None]:
        """
        ユーザーをフォローします
        Returns
        -------
        bool
            成功ならTrue, 失敗ならFalse
        str
            実行に失敗した際のエラーコード
        """

        if self.id:
            raise NotExistRequiredData('user_idがありません')
        return await self._state.user.follow.add(user_id=self.id)

    async def unfollow(self, user_id: str | None = None) -> bool:
        """
        与えられたIDのユーザーのフォローを解除します

        Parameters
        ----------
        user_id : str | None = None
            フォローを解除したいユーザーのID

        Returns
        -------
        status
            成功ならTrue, 失敗ならFalse
        """

        if user_id is None:
            user_id = self.user.id
        return await self._state.user.follow.remove(user_id)


class Header:
    def __init__(self, data):
        self.id = data.get('id')
        self.type = data.get('type')


class NoteReaction:
    __slots__ = ('__reaction', '__client')

    def __init__(self, reaction: INoteReaction, *, client: ClientManager):
        self.__reaction: INoteReaction = reaction
        self.__client: ClientManager = client

    @property
    def id(self) -> str | None:
        return self.__reaction['id']

    @property
    def created_at(self) -> datetime | None:
        return (
            datetime.strptime(
                self.__reaction['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
            )
            if 'created_at' in self.__reaction
            else None
        )

    @property
    def type(self) -> str | None:
        return self.__reaction['type']

    @property
    def user(self) -> LiteUser:
        return LiteUser(self.__reaction['user'], client=self.__client)


class Note:
    """
    Noteモデル

    Parameters
    ----------
    note: INote
        アクションを持たないNoteクラス
    client: ClientManager
    """

    def __init__(self, note: INote, client: ClientManager):
        self.__note = note
        self._client: ClientManager = client

    @property
    def id(self) -> str:
        """
        ユーザーのID

        Returns
        -------
        str
            ユーザーのID
        """
        return self.__note['id']

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self.__note['created_at'])

    @property
    def content(self) -> str | None:
        return self.__note.get('text')

    @property
    def cw(self) -> str | None:
        return self.__note.get('cw')

    @property
    def user_id(self) -> str:
        return self.__note['user_id']

    @property
    def author(self) -> LiteUser:
        return LiteUser(self.__note['user'], client=self._client)

    @property
    def reply_id(self) -> str:
        return self.__note['reply_id']

    @property
    def renote_id(self) -> str:
        return self.__note['renote_id']

    @property
    def files(self) -> list[IDriveFile]:  # TODO: モデルに
        return self.__note['files']

    @property
    def file_ids(self) -> list[str]:
        return self.__note['file_ids']

    @property
    def visibility(
        self,
    ) -> Literal['public', 'home', 'followers', 'specified']:
        return self.__note['visibility']

    @property
    def reactions(self) -> dict[str, int]:
        return self.__note['reactions']

    @property
    def renote_count(self) -> int:
        return self.__note['renote_count']

    @property
    def replies_count(self) -> int:
        return self.__note['replies_count']

    @property
    def emojis(self) -> list[ICustomEmojiLite]:  # TODO: モデルに
        """
        Note text contains a list of emojis
        Note: emojis have been abolished since misskey v13

        Returns
        -------
        list[ICustomEmojiLite]
            List of emojis contained in note text
        """

        return self.__note.get('emojis', [])

    @property
    def renote(self) -> 'Note' | None:
        return (
            Note(note=self.__note['renote'], client=self._client)
            if 'renote' in self.__note
            else None
        )

    @property
    def reply(self) -> 'Note' | None:
        return (
            Note(note=self.__note['renote'], client=self._client)
            if 'renote' in self.__note
            else None
        )

    @property
    def visible_user_ids(self) -> list[str]:
        return (
            self.__note['visible_user_ids']
            if 'visible_user_ids' in self.__note
            else []
        )

    @property
    def local_only(self) -> bool:
        return (
            self.__note['local_only'] if 'local_only' in self.__note else False
        )

    @property
    def my_reaction(self) -> str | None:
        return (
            self.__note['my_reaction']
            if 'my_reaction' in self.__note
            else None
        )

    @property
    def uri(self) -> str | None:
        return self.__note['uri'] if 'uri' in self.__note else None

    @property
    def url(self) -> str | None:
        return self.__note['url'] if 'url' in self.__note else None

    @property
    def is_hidden(self) -> bool:
        return (
            self.__note['is_hidden'] if 'is_hidden' in self.__note else False
        )

    @property
    def poll(self) -> Poll | None:
        return (
            Poll(self.__note['poll'], client=self._client)
            if 'poll' in self.__note
            else None
        )

    @property
    def api(self) -> ClientNoteManager:
        """
        ノートに対するアクション

        Returns
        -------
        NoteActions
        """
        return self._client.note.create_client_note_manager(self.id)


class NoteTranslateResult:
    """
    NoteTranslateResult

    Parameters
    ----------
    translate_result: INoteTranslateResult
        The raw data of the note translate result
    """

    def __init__(self, translate_result: INoteTranslateResult):
        self.__translate_result = translate_result

    @property
    def source_language(self) -> str:
        return self.__translate_result['sourceLang']

    @property
    def text(self) -> str:
        return self.__translate_result['text']
