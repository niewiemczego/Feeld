from typing import Any

from feeld.models.base import BaseResponse, InnerResponse


class ChatSummary(InnerResponse):
    id: str | None = None
    name: str | None = None
    type: str | None = None
    status: str | None = None
    avatar_set: list[str] | None = None
    member_count: int | None = None
    latest_message: str | None = None
    stream_channel_id: str | None = None
    target_profile_id: str | None = None


class PageInfo(InnerResponse):
    has_next_page: bool | None = None
    next_page_cursor: str | None = None


class PaginatedChatSummaries(InnerResponse):
    nodes: list[ChatSummary] | None = None
    page_info: PageInfo | None = None


class HeadSummariesResponse(BaseResponse):
    summaries: PaginatedChatSummaries | None = None

    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> "HeadSummariesResponse | None":
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
                        "id": "chat#289fba78-bc5a-43b2-adce-b6425b8285a1",
                        "name": "Bolz",
                        "type": "PRIVATE",
                        "status": "INACTIVE",
                        "avatarSet": [
                            "https://res.cloudinary.com/threender/image/upload/v1716647536/d689b171-84e0-40f5-b162-70fb35200a18.jpg"
                        ],
                        "memberCount": 2,
                        "latestMessage": None,
                        "streamChannelId": "2f5d28a0-aae7-489d-967e-4512a8240465",
                        "targetProfileId": "profile#71224273-98bd-4d44-bcfa-b84840c69772",
                        "__typename": "ChatSummary",
                    },
                    {
                        "id": "chat#f42ed321-50f2-44ca-b697-e240d92b59b3",
                        "name": "Beard",
                        "type": "PRIVATE",
                        "status": "INACTIVE",
                        "avatarSet": [
                            "https://res.cloudinary.com/threender/image/upload/v1702112713/3936fef0-57cf-4334-b3b4-36c080de00c0.jpg"
                        ],
                        "memberCount": 2,
                        "latestMessage": None,
                        "streamChannelId": "084da348-88d0-4726-b459-06a84b49ba1d",
                        "targetProfileId": "profile#2aa4dc40-1579-45f6-97da-6579393e3199",
                        "__typename": "ChatSummary",
                    },
                ],
                "pageInfo": {
                    "hasNextPage": True,
                    "nextPageCursor": "eyJzayI6ImludGVyYWN0aW9uX3R5cGUjbGlrZXx0YXJnZXQjcHJvZmlsZSMyZGI5MGUyOS04ODhiLTRkNGQtOWFhZC05Njc1YTY1ZmM3MGMiLCJwayI6InNvdXJjZSNwcm9maWxlIzU5OTcxNTdhLWMzMzEtNWYzMC1iYjg3LWVmZGIzNTcwZTMyNyIsInRhcmdldCI6InByb2ZpbGUjMmRiOTBlMjktODg4Yi00ZDRkLTlhYWQtOTY3NWE2NWZjNzBjIiwidGltZXN0YW1wIjoxNzI1NDkyNjM4NDg2fQ==",
                    "__typename": "PageInfo",
                },
                "__typename": "PaginatedChatSummaries",
            }
        },
        "extensions": {"requestId": "88724777-fe78-4d38-b288-36aab3cc2520"},
    }

    response = HeadSummariesResponse.parse_response(data)
    print(response)
