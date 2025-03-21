import logging
from typing import Any

from feeld.chat.models.chat_create import ChatCreateResponse
from feeld.chat.models.chat_summaries import ChatSummariesResponse
from feeld.networking.http_manager import HTTPManager


class ChatManager:
    _logger = logging.getLogger(__name__)

    def __init__(self, http_manager: HTTPManager) -> None:
        self._http_manager = http_manager

    async def get_chat_summaries(
        self, limit: int = 10, next_page_cursor: str | None = None
    ) -> ChatSummariesResponse | None:
        """
        limit must not be greater than 30
        """
        payload = {
            "operationName": "ListSummaries",
            "variables": {"limit": limit} if next_page_cursor is None else {"limit": limit, "cursor": next_page_cursor},
            "query": "query ListSummaries($limit: Int = "
            + str(limit)
            + ", $cursor: String) {\n  summaries: getChatSummariesForChatList(limit: $limit, cursor: $cursor) {\n    nodes {\n      ...ChatSummaryItem\n      __typename\n    }\n    pageInfo {\n      hasNextPage\n      nextPageCursor\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ChatSummaryItem on ChatSummary {\n  id\n  name\n  type\n  status\n  avatarSet\n  memberCount\n  latestMessage\n  streamChannelId\n  targetProfileId\n  __typename\n}",
        }
        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return None

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to get chat summaries - Unknown error[{res.status_code}]")
            return None

        return ChatSummariesResponse.parse_response(res.json())

    async def disconnect_from_chat(self, chat_id: str) -> bool:
        payload = {
            "operationName": "DisconnectFromChat",
            "variables": {"input": {"chatId": chat_id}},
            "query": "mutation DisconnectFromChat($input: ChatDisconnectInput!) {\n  disconnectFromChat(input: $input) {\n    chatId\n    __typename\n  }\n}",
        }
        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return False

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to disconnect from chat - Unknown error[{res.status_code}]")
            return False

        return True

    async def create_chat(self, profile_id: str) -> ChatCreateResponse | None:
        payload = {
            "operationName": "ChatCreate",
            "variables": {"input": {"targetProfileIds": [profile_id]}},
            "query": "mutation ChatCreate($input: ChatCreateInput!) {\n  chatCreate(input: $input) {\n    ...ChatSummaryItem\n    __typename\n  }\n}\n\nfragment ChatSummaryItem on ChatSummary {\n  id\n  name\n  type\n  status\n  avatarSet\n  memberCount\n  latestMessage\n  streamChannelId\n  targetProfileId\n  __typename\n}",
        }
        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return None

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to create chat - Unknown error[{res.status_code}]")
            return None

        return ChatCreateResponse.parse_response(res.json())

    async def activate_chat(self, chat_id: str) -> dict[str, Any] | None:
        payload = {
            "operationName": "ChatActivate",
            "variables": {"input": {"chatId": chat_id}},
            "query": "mutation ChatActivate($input: ChatActivateInput!) {\n  chatActivate(input: $input) {\n    id\n    streamChatId\n    __typename\n  }\n}",
        }

        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return None

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to create chat - Unknown error[{res.status_code}]")
            return None

        return res.json()
