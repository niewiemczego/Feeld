from datetime import datetime
from typing import Any

from pydantic import Field

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
    attachments: list | None = None
    latest_reactions: list | None = None
    own_reactions: list | None = None
    reaction_counts: dict | None = None
    reaction_scores: dict | None = None
    reply_count: int | None = None
    deleted_reply_count: int | None = None
    cid: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    shadowed: bool | None = None
    mentioned_users: list | None = None
    silent: bool | None = None
    pinned: bool | None = None
    pinned_at: datetime | None = None
    pinned_by: str | None = None
    pin_expires: datetime | None = None
    custom_properties: CustomProperties | None = None
    html_: str | None = Field(default=None, alias="__html")
    status: str | None = None


class ChatSummary(InnerResponse):
    id: str | None = None
    name: str | None = None
    type: str | None = None
    status: str | None = None
    avatar_set: list[str] | None = None
    member_count: int | None = None
    latest_message: LatestMessage | None = None
    stream_channel_id: str | None = None
    target_profile_id: str | None = None


class ChatSummaryResponse(BaseResponse):
    summary: ChatSummary | None = None

    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> "ChatSummaryResponse | None":
        try:
            return cls(summary=data["data"]["summary"])
        except (TypeError, KeyError) as e:
            print(f"Missing key {e}: {data}")
            return None


if __name__ == "__main__":
    data = {
        "data": {
            "summary": {
                "id": "chat#50e250be-6105-48d2-ad41-a13d1b140438",
                "name": "Vittorio 🇮🇹",
                "type": "PRIVATE",
                "status": "INACTIVE",
                "avatarSet": [
                    "https://res.cloudinary.com/threender/image/upload/v1706363168/f7870b5d-c843-4afd-854d-254a2e069d95.jpg"
                ],
                "memberCount": 2,
                "latestMessage": {
                    "id": "b166d718-3e4e-4de7-9cc4-99617c0c7e42",
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
                    "cid": "messaging:2e5ffee4-b458-4318-b0ca-39d5b77be655",
                    "created_at": "2024-09-05T12:00:06.753Z",
                    "updated_at": "2024-09-05T12:00:06.753Z",
                    "shadowed": False,
                    "mentioned_users": [],
                    "silent": False,
                    "pinned": False,
                    "pinned_at": None,
                    "pinned_by": None,
                    "pin_expires": None,
                    "custom_properties": {
                        "user_ids": ["45340f72-682a-406a-997b-b67df990dc8f", "61c5ca53b59d4d0043014e1a"],
                        "event_type": "new_match",
                        "snapshot": {
                            "users": [
                                {"name": "Jagoda", "streamUserId": "45340f72-682a-406a-997b-b67df990dc8f"},
                                {"name": "Vittorio 🇮🇹", "streamUserId": "61c5ca53b59d4d0043014e1a"},
                            ]
                        },
                    },
                    "__html": "",
                    "status": "received",
                },
                "streamChannelId": "2e5ffee4-b458-4318-b0ca-39d5b77be655",
                "targetProfileId": "profile#f96a78c2-a012-5e67-b76b-3dab7f579b58",
                "__typename": "ChatSummary",
            }
        },
        "extensions": {"requestId": "95155dff-bc30-472c-a58f-70a2a461ea78"},
    }

    response = ChatSummaryResponse.parse_response(data)
    print(response)
