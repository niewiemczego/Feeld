from typing import Any

from feeld.models.base import BaseResponse, InnerResponse


class UploadCredentials(InnerResponse):
    public_id: str | None = None
    signature: str | None = None
    timestamp: int | None = None


class GenerateUploadCredentialsResponse(BaseResponse):
    data: UploadCredentials | None = None

    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> "GenerateUploadCredentialsResponse | None":
        try:
            return cls(data=data["data"]["cloudinaryGenerateUploadCredentials"])
        except (TypeError, KeyError) as e:
            print(f"Missing key {e}: {data}")
            return None


if __name__ == "__main__":
    data = {
        "data": {
            "cloudinaryGenerateUploadCredentials": {
                "publicId": "e17806e1-59b4-480b-bc33-0277f3fad851",
                "signature": "f224776205e6a513a5ee236d7604ff9a1c1d735a",
                "timestamp": 1725653617671,
                "__typename": "CloudinarySignature",
            }
        },
        "extensions": {"requestId": "0bc3c06e-6bfa-46ba-b3d4-351fb7392043"},
    }

    response = GenerateUploadCredentialsResponse.parse_response(data)
    print(response)
