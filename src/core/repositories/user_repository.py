import json
from typing import Type, TypeVar, Generic
from collections.abc import Collection

from src.core.storage.base import Storage

from src.core.client.base import User, Track, Artist
from dataclasses import asdict

UserClassT = TypeVar("UserClassT", bound=User)


class InvalidJsonException(Exception):
    pass


class UserRepository(Generic[UserClassT]):
    def __init__(self, user_cls: Type[UserClassT], storage: Storage) -> None:
        self._storage = storage
        self._user_cls = user_cls

    def _get_user_object(self, raw_user: str) -> UserClassT:
        try:
            user_dict = json.loads(raw_user)
        except json.JSONDecodeError:
            raise InvalidJsonException(
                f"Error when parsing user, not valid JSON: \n{raw_user}"
            )
        user = self._user_cls(**user_dict)
        return user

    def get_user(self, user_id: str) -> UserClassT | None:
        user_raw = self._storage.read(f"user:{user_id}")

        if not user_raw:
            return None

        user = self._get_user_object(user_raw)
        return user

    def get_user_id(self, user_email: str) -> str | None:
        user_id: bytes | None = self._storage.read(f"user:email:{user_email}")
        return user_id.decode() if user_id else None

    def get_user_by_email(
        self, user_email: str
    ) -> tuple[str | None, UserClassT | None]:
        user_id = self.get_user_id(user_email)

        if user_id is None:
            return None, None

        return user_id, self.get_user(user_id)

    def get_users(self, user_ids: Collection[str]) -> list[UserClassT]:
        users_raw: list[str | None] = self._storage.read_many(
            [f"user:{u_id}" for u_id in user_ids]
        )
        users: list[UserClassT] = []

        for user_raw in users_raw:
            if user_raw is None:
                continue
            users.append(self._get_user_object(user_raw))

        return users

    def get_user_session(self, user_id: str) -> list[UserClassT]:
        session_raw = self._storage.read(f"session:{user_id}")

        if not session_raw:
            return []

        try:
            session: list[str] = json.loads(session_raw)
        except json.JSONDecodeError:
            raise InvalidJsonException(
                f"Error when parsing session, not valid JSON: \n{session_raw}"
            )

        users = self.get_users(session)

        return users

    def add_to_session(self, owner_id: str, new_user_id: str) -> None:
        session_key = f"session:{owner_id}"
        session: list[str] = json.loads(self._storage.read(session_key) or "[]")

        if new_user_id not in session:
            session.append(new_user_id)
            self._storage.write(f"session:{owner_id}", json.dumps(session))

    def remove_from_session(self, owner_id: str, remove_user_id: str) -> None:
        session_key = f"session:{owner_id}"
        session: list[str] = json.loads(self._storage.read(session_key) or "[]")

        if len(session) == 0:
            raise ValueError("Session is already empty.")

        if remove_user_id not in session:
            raise ValueError(f"User {remove_user_id} not in session.")

        del session[session.index(remove_user_id)]
        self._storage.write(f"session:{owner_id}", json.dumps(session))

    def save_user(self, user: UserClassT) -> None:
        self._storage.write(f"user:{user.id}", json.dumps(asdict(user)))
        self._storage.write(f"user:email:{user.email}", user.id)

    def delete_user(self, user_id: str) -> None:
        user = self.get_user(user_id)
        if not user:
            return

        self._storage.delete(f"user:{user_id}")
        self._storage.delete(f"user:email:{user.email}")
        self._storage.delete(f"session:{user_id}")

    def get_blend(self, user_id: str) -> list[Track]:
        blend_raw = self._storage.read(f"blend:{user_id}")
        if not blend_raw:
            return []

        blend_dict = json.loads(blend_raw)

        blend: list[Track] = []
        for track_dict in blend_dict:
            artists = [Artist(**a) for a in track_dict["artists"]]
            del track_dict["artists"]
            blend.append(Track(**track_dict, artists=artists))

        return blend

    def save_blend(self, user_id: str, blend: list[Track]) -> None:
        blend_dicts = [asdict(t) for t in blend]
        self._storage.write(f"blend:{user_id}", json.dumps(blend_dicts))
