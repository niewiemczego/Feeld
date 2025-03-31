from datetime import datetime
from typing import Any

from pydantic import Field

from feeld.models.base import BaseResponse, InnerResponse


class UploadData(InnerResponse):
    attachment_id: str | None = Field(default=None, alias="attachmentID")
    chat_id: str | None = Field(default=None, alias="chatID")
    created_at: datetime | None = None
    creator_id: str | None = Field(default=None, alias="creatorID")
    provider_asset_id: str | None = Field(default=None, alias="providerAssetID")
    provider_source: str | None = None
    updated_at: datetime | None = None
    visibility_milliseconds: int | None = None


class UploadChatAttachmentResponse(BaseResponse):
    data: UploadData | None = None

    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> "UploadChatAttachmentResponse | None":
        try:
            return cls(data=data["data"]["uploadChatAttachment"])
        except (TypeError, KeyError) as e:
            print(f"Missing key {e}: {data}")
            return None


if __name__ == "__main__":
    data = {
        "data": {
            "uploadChatAttachment": {
                "attachmentID": "chat-attachment#93bbdba0-e884-4857-b62b-bd95f11e81de",
                "chatID": "chat#6b2959f9-a1a8-4dab-88b9-817b7715e76d",
                "createdAt": "2024-09-06T20:13:39.678Z",
                "creatorID": "profile#2db90e29-888b-4d4d-9aad-9675a65fc70c",
                "providerAssetID": "e17806e1-59b4-480b-bc33-0277f3fad851",
                "providerSource": "Cloudinary",
                "updatedAt": "2024-09-06T20:13:39.678Z",
                "visibilityMilliseconds": None,
                "__typename": "GQLChatAttachmentOutput",
            }
        },
        "extensions": {"requestId": "b388d59b-dcb8-4bbc-a233-42bc7b80d604"},
    }

    response = UploadChatAttachmentResponse.parse_response(data)
    print(response)
