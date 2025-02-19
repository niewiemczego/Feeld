from datetime import datetime
from typing import Any

from feeld.models.base import BaseResponse, InnerResponse
from feeld.models.desires import DesiresType
from feeld.models.gender import GenderType
from feeld.models.looking_for import LookingForType
from feeld.models.sexuality import SexualityType


class ProfileCreateData(InnerResponse):
    bio: str | None = None
    date_of_birth: datetime | None = None
    desires: list[DesiresType] | None = None
    gender: GenderType | None = None
    imaginary_name: str | None = None
    interests: list[str] | None = None
    id: str | None = None
    sexuality: SexualityType | None = None
    looking_for: list[LookingForType] | None = None
    status: str | None = None
    stream_token: str | None = None
    stream_user_id: str | None = None


class ProfileCreateResponse(BaseResponse):
    data: ProfileCreateData | None = None

    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> "ProfileCreateResponse | None":
        try:
            return cls(data=data["data"]["profileCreate"])
        except (TypeError, KeyError) as e:
            print(f"Missing key {e}: {data}")
            return None


if __name__ == "__main__":
    payload = {
        "data": {
            "profileCreate": {
                "bio": None,
                "dateOfBirth": "1990-12-31T00:00:00.000Z",
                "desires": [
                    "MONOGAMY",
                    "FWB",
                    "FUN",
                    "BRAT_TAMER",
                    "DOMINANTS",
                    "EDGING",
                    "BRAT",
                    "KINK",
                    "CASUAL",
                    "DATES",
                ],
                "gender": "WOMAN",
                "imaginaryName": "Sharllote",
                "interests": [],
                "id": "profile#99d2eb5f-8814-402f-b418-99fb1313c530",
                "sexuality": "STRAIGHT",
                "lookingFor": None,
                "status": "INCOMPLETE",
                "streamToken": None,
                "streamUserId": "b3de7b44-1828-45a7-84b9-ea6e444151c3",
                "__typename": "Profile",
            }
        },
        "extensions": {"requestId": "8ca5b696-f50b-414f-8908-5f0ba9ff8ebb"},
    }
