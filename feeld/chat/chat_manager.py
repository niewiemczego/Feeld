import logging
from typing import Any

from requests_toolbelt.multipart.encoder import MultipartEncoder

from feeld.chat.models.chat_create import ChatCreateResponse
from feeld.chat.models.chat_message import ImageMessage, TextMessage, VideoMessage
from feeld.chat.models.chat_summaries import ChatSummariesResponse
from feeld.chat.models.generate_upload_credentials import GenerateUploadCredentialsResponse
from feeld.chat.models.upload_chat_attachment import UploadChatAttachmentResponse
from feeld.core.helpers import get_file_content_type, get_video_duration
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

    async def get_connection_id(self) -> str | None:
        """
        Gets the connection id needed for the chat related requests
        """
        res = await self._http_manager._request(
            "GET",
            f"{self._http_manager._BASE_CHAT_URL}/longpoll?user_id={self._http_manager._stream_id}&api_key=y4tp4akjeb49&json=%7B%22user_id%22%3A%22{self._http_manager._stream_id}%22%2C%22user_details%22%3A%7B%22id%22%3A%22{self._http_manager._stream_id}%22%7D%7D",
            headers=self._http_manager._default_headers_chat,
        )
        if res is None:
            return None

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to get connection id - Unknown error[{res.status_code}]")
            return None

        return res.json().get("event", {}).get("connection_id")

    async def get_messages_history(
        self, user_stream_channel_id: str, connection_id: str, limit: int = 50
    ) -> list[dict[str, Any]] | None:
        payload = {"data": {}, "state": True, "watch": True, "presence": False, "messages": {"limit": limit}}
        res = await self._http_manager._request(
            "POST",
            f"{self._http_manager._BASE_CHAT_URL}/channels/messaging/{user_stream_channel_id}/query?user_id={self._http_manager._stream_id}&connection_id={connection_id}&api_key=y4tp4akjeb49",
            headers=self._http_manager._default_headers_chat,
            json=payload,
        )
        if res is None:
            return None

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 201 or "errors" in res.json():
            self._logger.error(f"Failed to get messsages history - Unknown error[{res.status_code}]")
            return None

        return res.json().get("messages")

    async def create_picture(self, public_id: str, picture_order: int, is_secondary: bool) -> dict[str, Any] | None:
        payload = {
            "operationName": "PictureCreate",
            "variables": {
                "input": {
                    "profileId": self._http_manager.profile_id,
                    "publicId": public_id,
                    "pictureType": "SECONDARY" if is_secondary else "DEFAULT",
                    "pictureOrder": picture_order,
                }
            },
            "query": "mutation PictureCreate($input: PictureCreateInput!) {\n  pictureCreate(input: $input) {\n    ...PictureCreateFragment\n    __typename\n  }\n}\n\nfragment PictureCreateFragment on Picture {\n  id\n  pictureIsPrivate\n  pictureIsSafe\n  pictureOrder\n  pictureScore\n  pictureStatus\n  pictureType\n  pictureUrl\n  profileId\n  publicId\n  __typename\n}",
        }
        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, headers=self._http_manager._default_headers, json=payload
        )
        if res is None:
            return None

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to create picture - Unknown error[{res.status_code}]")
            return None

        return res.json()

    async def generate_upload_credentials_for_attachment(self) -> GenerateUploadCredentialsResponse | None:
        payload = {
            "operationName": "CloudinaryGenerateUploadCredentials",
            "variables": {},
            "query": "mutation CloudinaryGenerateUploadCredentials {\n  cloudinaryGenerateUploadCredentials {\n    publicId\n    signature\n    timestamp\n    __typename\n  }\n}",
        }
        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, headers=self._http_manager._default_headers, json=payload
        )
        if res is None:
            return None

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to generate upload credentials - Unknown error[{res.status_code}]")
            return None

        return GenerateUploadCredentialsResponse.parse_response(res.json())

    async def upload_attachment(
        self, upload_credentials: GenerateUploadCredentialsResponse, image_path: str
    ) -> dict[str, Any] | None:
        mp_encoder = MultipartEncoder(
            fields={
                "api_key": "578158198623524",
                "timestamp": str(upload_credentials.data.timestamp),
                "public_id": upload_credentials.data.public_id,
                "signature": upload_credentials.data.signature,
                "file": (image_path.split("/")[-1], open(image_path, "rb"), get_file_content_type(image_path)),
            }
        )
        # Since we are uplading image to cloudinary server we dont need to use proxy and that way we save a lot of proxy data
        proxy = self._http_manager._session.proxies.copy()
        self._http_manager._session.proxies = {}

        res = await self._http_manager._request(
            "POST",
            "https://api.cloudinary.com/v1_1/threender/upload",
            data=mp_encoder.to_string(),
            headers={"Content-Type": mp_encoder.content_type},
        )
        self._http_manager._session.proxies = proxy

        if res is None:
            return None

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to upload attachment - Unknown error[{res.status_code}]")
            return None

        return res.json()

    async def upload_attachment_to_chat(
        self, chat_id: str, public_id: str, visibility_in_ms: int | None = None
    ) -> UploadChatAttachmentResponse | None:
        payload = {
            "operationName": "UploadChatAttachment",
            "variables": {
                "input": {
                    "chatID": chat_id,
                    "creatorID": self._http_manager.profile_id,
                    "providerAssetID": public_id,
                    "providerSource": "Cloudinary",
                    "visibilityMilliseconds": visibility_in_ms,
                }
            },
            "query": "mutation UploadChatAttachment($input: GQLChatAttachmentUploadInput!) {\n  uploadChatAttachment(input: $input) {\n    attachmentID\n    chatID\n    createdAt\n    creatorID\n    providerAssetID\n    providerSource\n    updatedAt\n    visibilityMilliseconds\n    __typename\n  }\n}",
        }
        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, headers=self._http_manager._default_headers, json=payload
        )
        if res is None:
            return None

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            print(f"Failed to upload attachment to chat - Unknown error[{res.status_code}]")
            return None

        return UploadChatAttachmentResponse.parse_response(res.json())

    async def send_text_message(self, user_stream_channel_id: str, connection_id: str, message: TextMessage) -> bool:
        res = await self._send_message_to_chat(user_stream_channel_id, connection_id, message)
        if res is None:
            return False

        return True

    async def send_image_message(
        self, user_stream_channel_id: str, connection_id: str, image_path: str, chat_id: str, message: ImageMessage
    ) -> bool:
        visibility_in_ms = message.playable_duration * 1000 if message.playable_duration else message.playable_duration
        upload_image_data = await self.upload_image(image_path, chat_id, visibility_in_ms)
        if upload_image_data is None:
            return False

        message.attachment_id = upload_image_data.data.attachment_id

        res = await self._send_message_to_chat(user_stream_channel_id, connection_id, message)
        if res is None:
            return False

        return True

    async def upload_image(
        self, image_path: str, chat_id: str, visibility_in_ms: int | None = None
    ) -> UploadChatAttachmentResponse | None:
        credentials = await self.generate_upload_credentials_for_attachment()
        if credentials is None:
            return None

        upload_attachment_data = await self.upload_attachment(credentials, image_path)
        if upload_attachment_data is None:
            return None

        upload_to_chat = await self.upload_attachment_to_chat(chat_id, credentials.data.public_id, visibility_in_ms)
        if upload_to_chat is None:
            return None

        return upload_to_chat

    async def send_video_message(
        self, user_stream_channel_id: str, connection_id: str, video_path: str, message: VideoMessage
    ) -> dict[str, Any] | None:
        """
        Fun fact - you can send video longer than 15 seconds, they only limit it via app client
        """
        url = await self.upload_video(user_stream_channel_id, connection_id, video_path)
        if url is None:
            return

        video_duration = get_video_duration(video_path)

        message.url = url
        message.duration = video_duration

        return await self._send_message_to_chat(user_stream_channel_id, connection_id, message)

    async def upload_video(self, user_stream_channel_id: str, connection_id: str, video_path: str) -> str | None:
        mp_encoder = MultipartEncoder(
            fields={
                "file": (video_path.split("/")[-1], open(video_path, "rb"), get_file_content_type(video_path)),
            }
        )
        res = await self._http_manager._request(
            "POST",
            f"https://chat.stream-io-api.com/channels/messaging/{user_stream_channel_id}/file?user_id={self._http_manager._stream_id}&connection_id={connection_id}&api_key=y4tp4akjeb49",
            headers=self._http_manager._default_headers_chat | {"Content-Type": mp_encoder.content_type},
            data=mp_encoder.to_string(),
        )
        if res is None:
            return None

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 201:
            self._logger.error(f"Failed to send message to chat - Unknown error[{res.status_code}]")
            return None

        return res.json().get("file")

    async def _send_message_to_chat(
        self, user_stream_channel_id: str, connection_id: str, message: TextMessage | ImageMessage | VideoMessage
    ) -> dict[str, Any] | None:
        res = await self._http_manager._request(
            "POST",
            f"https://chat.stream-io-api.com/channels/messaging/{user_stream_channel_id}/message?user_id={self._http_manager._stream_id}&connection_id={connection_id}&api_key=y4tp4akjeb49",
            headers=self._http_manager._default_headers_chat,
            json=message.to_payload_dict(),
        )
        if res is None:
            return None

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 201:
            self._logger.error(f"Failed to send message to chat - Unknown error[{res.status_code}]")
            return None

        return res.json()
