from datetime import datetime
from typing import Any

from feeld.models.base import BaseResponse, InnerResponse


class User(InnerResponse):
    id: str | None = None
    language: str | None = None
    role: str | None = None
    teams: list[str] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    banned: bool | None = None
    online: bool | None = None
    blocked_user_ids: list[str] | None = None
    shadow_banned: bool | None = None
    invisible: bool | None = None


class SnapshotUser(InnerResponse):
    name: str | None = None
    stream_user_id: str | None = None


class Snapshot(InnerResponse):
    users: list[SnapshotUser] | None = None


class CustomProperties(InnerResponse):
    user_ids: list[str] | None = None
    event_type: str | None = None
    snapshot: Snapshot | None = None


class LatestMessage(InnerResponse):
    id: str | None = None
    text: str | None = None
    html: str | None = None
    type: str | None = None
    user: User | None = None
    attachments: list[Any] | None = None
    latest_reactions: list[Any] | None = None
    own_reactions: list[Any] | None = None
    reaction_counts: dict[str, int] | None = None
    reaction_scores: dict[str, int] | None = None
    reply_count: int | None = None
    deleted_reply_count: int | None = None
    cid: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    shadowed: bool | None = None
    mentioned_users: list[Any] | None = None
    silent: bool | None = None
    pinned: bool | None = None
    pinned_at: datetime | None = None
    pinned_by: Any | None = None
    pin_expires: datetime | None = None
    custom_properties: CustomProperties | None = None
    status: str | None = None


class ChatCreate(InnerResponse):
    id: str | None = None
    name: str | None = None
    type: str | None = None
    status: str | None = None
    avatar_set: list[str] | list[None] | str | None = None
    member_count: int | None = None
    latest_message: LatestMessage | None = None
    stream_channel_id: str | None = None
    target_profile_id: str | None = None


class ChatCreateResponse(BaseResponse):
    chat_create: ChatCreate | None = None

    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> "ChatCreateResponse | None":
        try:
            return cls(chat_create=data["data"]["chatCreate"])
        except (KeyError, TypeError) as e:
            print(f"Error {e}: {data}")
            return None


if __name__ == "__main__":
    data = {
        "data": {
            "chatCreate": {
                "id": "chat#ebd7d7e6-448b-45e1-b792-bb29fe5deea2",
                "name": "Kirill & Pati",
                "type": "PRIVATE",
                "status": "INACTIVE",
                "avatarSet": ["https://res.cloudinary.com/threender/image/upload/a0255dc5-e3cf-45c4-b2f4-354f2c2f30dc"],
                "memberCount": 2,
                "latestMessage": {
                    "id": "0e3e570b-0dba-4e89-bfe3-f33d55dce12f",
                    "text": "",
                    "html": "",
                    "type": "system",
                    "user": {
                        "id": "STREAM_SYSTEM_ADMIN_USER",
                        "language": "",
                        "role": "user",
                        "teams": [],
                        "created_at": "2024-01-15T16:56:35.194153Z",
                        "updated_at": "2024-01-15T16:56:35.194153Z",
                        "banned": False,
                        "online": False,
                        "blocked_user_ids": [],
                        "shadow_banned": False,
                        "invisible": False,
                    },
                    "attachments": [],
                    "latest_reactions": [],
                    "own_reactions": [],
                    "reaction_counts": {},
                    "reaction_scores": {},
                    "reply_count": 0,
                    "deleted_reply_count": 0,
                    "cid": "messaging:0d9355fa-0731-45d3-b7ee-590e172b3b03",
                    "created_at": "2024-10-26T11:43:21.909Z",
                    "updated_at": "2024-10-26T11:43:21.909Z",
                    "shadowed": False,
                    "mentioned_users": [],
                    "silent": False,
                    "pinned": False,
                    "pinned_at": None,
                    "pinned_by": None,
                    "pin_expires": None,
                    "custom_properties": {
                        "user_ids": ["0eb15f75-7b35-4e5b-bdc4-dbfc46aafad5", "d2d1f094-fda4-48b8-b418-c1fea75d4f75"],
                        "event_type": "new_match",
                        "snapshot": {
                            "users": [
                                {"name": "Suzy", "streamUserId": "0eb15f75-7b35-4e5b-bdc4-dbfc46aafad5"},
                                {"name": "Kirill & Pati", "streamUserId": "d2d1f094-fda4-48b8-b418-c1fea75d4f75"},
                            ]
                        },
                    },
                    "status": "received",
                },
                "streamChannelId": "0d9355fa-0731-45d3-b7ee-590e172b3b03",
                "targetProfileId": "profile#9786e52d-e7c3-422a-8408-f39b58fc9010",
                "__typename": "ChatSummary",
            }
        },
        "extensions": {"requestId": "856351d8-d5c7-4f04-9cd7-034a8899f38d"},
    }

    response = ChatCreateResponse.parse_response(data)
    print(response)
