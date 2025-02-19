from datetime import datetime
from typing import Any

from pydantic import Field

from feeld.models.base import BaseResponse, InnerResponse


class User(InnerResponse):
    id: str | None = None
    name: str | None = None
    image: str | None = None
    language: str | None = None
    role: str | None = None
    teams: list[str] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    banned: bool | None = None
    online: bool | None = None
    last_active: datetime | None = None
    blocked_user_ids: list[str] | None = None
    shadow_banned: bool | None = None
    invisible: bool | None = None
    profile_status: str | None = None
    profile_is_incognito: bool | None = None


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
    custom_properties: dict | None = None
    html: str | None = Field(default=None, alias="__html")
    status: str | None = None


class ChatSummary(InnerResponse):
    id: str | None = None
    name: str | None = None
    type: str | None = None
    status: str | None = None
    avatar_set: list[str] | list[None] | None = None
    member_count: int | None = None
    latest_message: LatestMessage | None = None
    stream_channel_id: str | None = None
    target_profile_id: str | None = None


class PageInfo(InnerResponse):
    has_next_page: bool | None = None
    next_page_cursor: str | None = None


class PaginatedChatSummaries(InnerResponse):
    nodes: list[ChatSummary] | None = None
    page_info: PageInfo | None = None


class ChatSummariesResponse(BaseResponse):
    summaries: PaginatedChatSummaries | None = None

    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> "ChatSummariesResponse | None":
        try:
            return cls(summaries=data["data"]["summaries"])
        except (TypeError, KeyError) as e:
            print(f"Missing key {e}: {data}")
            return None


if __name__ == "__main__":
    data = {
        "data": {
            "summaries": {
                "nodes": [
                    {
                        "id": "chat#d2bc39f6-cdd3-4f73-82d0-aa8bf9921b8a",
                        "name": "ReFresh",
                        "type": "PRIVATE",
                        "status": "ACTIVE",
                        "avatarSet": [
                            "https://res.cloudinary.com/threender/image/upload/v1681300404/cbf18775-497e-4987-ada6-5ae8151cb85a.jpg"
                        ],
                        "memberCount": 2,
                        "latestMessage": {
                            "id": "acbc87d5-53de-4fbc-adb7-e61d82b66267",
                            "text": "You are soo beautiful..!",
                            "html": "<p>You are soo beautiful..!</p>\n",
                            "type": "regular",
                            "user": {
                                "id": "61d2de36d254ff00430192cc",
                                "name": "ReFresh",
                                "image": "https://res.cloudinary.com/threender/image/upload/v1681300404/cbf18775-497e-4987-ada6-5ae8151cb85a.jpg",
                                "language": "",
                                "role": "user",
                                "teams": [],
                                "created_at": "2022-01-03T11:32:37.902413Z",
                                "updated_at": "2024-08-07T04:33:06.638769Z",
                                "banned": False,
                                "online": False,
                                "last_active": "2024-09-05T11:16:12.004473042Z",
                                "blocked_user_ids": [],
                                "shadow_banned": False,
                                "invisible": False,
                                "profileStatus": "active",
                                "profileIsIncognito": False,
                            },
                            "attachments": [],
                            "latest_reactions": [],
                            "own_reactions": [],
                            "reaction_counts": {},
                            "reaction_scores": {},
                            "reply_count": 0,
                            "deleted_reply_count": 0,
                            "cid": "messaging:01d3128f-b772-4571-a5db-29c4143982da",
                            "created_at": "2024-09-05T11:10:12.609Z",
                            "updated_at": "2024-09-05T11:10:12.609Z",
                            "shadowed": False,
                            "mentioned_users": [],
                            "silent": False,
                            "pinned": False,
                            "pinned_at": None,
                            "pinned_by": None,
                            "pin_expires": None,
                            "custom_properties": {"type": "text", "status": "regular"},
                            "__html": "<p>You are soo beautiful..!</p>\n",
                            "status": "received",
                        },
                        "streamChannelId": "01d3128f-b772-4571-a5db-29c4143982da",
                        "targetProfileId": "profile#d3e9ed21-4d4f-57d5-a3de-4ab27021ee0c",
                        "__typename": "ChatSummary",
                    },
                ],
                "pageInfo": {"hasNextPage": False, "nextPageCursor": None, "__typename": "PageInfo"},
                "__typename": "PaginatedChatSummaries",
            }
        },
        "extensions": {"requestId": "ec2e0bc3-a127-457c-8fed-dcd3c0561b0b"},
    }

    response = ChatSummariesResponse.parse_response(data)
    print(response)
