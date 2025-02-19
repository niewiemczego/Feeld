from datetime import datetime
from typing import Any

from feeld.models.base import BaseResponse, InnerResponse
from feeld.models.desires import DesiresType
from feeld.models.gender import GenderType
from feeld.models.looking_for import LookingForType
from feeld.models.sexuality import SexualityType


class ProfileUpdatePayload(InnerResponse):
    gender: GenderType | None = None
    desires: list[DesiresType] | None = None
    looking_for: list[LookingForType] | None = None
    sexuality: SexualityType | None = None
    imaginary_name: str | None = None
    date_of_birth: str | None = None
    bio: str | None = None
    interests: list[str] | None = None

    def _to_camel_case(self, snake_str: str) -> str:
        components = snake_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    def get_input_payload(self, additional_payload_data: dict[str, Any] | None = None) -> dict[str, Any]:
        input_payload = additional_payload_data if additional_payload_data else {}
        for key, value in self.__dict__.items():
            if value is not None:
                camel_case_key = self._to_camel_case(key)
                input_payload[camel_case_key] = value

        input_payload["allowPWM"] = True

        return input_payload


class ProfileUpdateData(InnerResponse):
    id: str | None = None
    age: int | None = None
    age_range: list | None = None
    allow_pwm: bool | None = None
    bio: str | None = None
    completion_status: str | None = None
    date_of_birth: datetime | None = None
    desires: list[str] | None = None
    distance_max: int | None = None
    gender: str | None = None
    imaginary_name: str | None = None
    interests: list[str] | None = None
    is_incognito: bool | None = None
    looking_for: list[str] | None = None
    recently_online: str | None = None
    sexuality: str | None = None
    status: str | None = None
    stream_token: str | None = None


class ProfileUpdateResponse(BaseResponse):
    data: ProfileUpdateData | None = None

    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> "ProfileUpdateResponse | None":
        try:
            return cls(data=data["data"]["profileUpdate"])
        except (TypeError, KeyError) as e:
            print(f"Missing key {e}: {data}")
            return None


if __name__ == "__main__":
    payload = {
        "data": {
            "profileUpdate": {
                "id": "profile#a80fb3b7-3c60-4015-9980-eb1881ca7369",
                "age": 23,
                "ageRange": [18, 99],
                "allowPWM": True,
                "bio": "Just don’t be shy okay? Im sure you won’t regret messaging me haha🙈",
                "completionStatus": "BIO",
                "dateOfBirth": "2000-12-31T00:00:00.000Z",
                "desires": [
                    "FWB",
                    "FUN",
                    "INTIMACY",
                    "OPEN_RELATIONSHIP",
                    "BDSM",
                    "ROUGH",
                    "ROLE_PLAY",
                    "SUBMISSIVES",
                    "THREESOME",
                    "COUPLES",
                ],
                "distanceMax": 100,
                "gender": "WOMAN",
                "imaginaryName": "Emma",
                "interests": [],
                "isIncognito": False,
                "lookingFor": [
                    "AGENDER",
                    "ANDROGYNOUS",
                    "BIGENDER",
                    "GENDER_FLUID",
                    "GENDER_NONCONFORMING",
                    "GENDER_QUEER",
                    "GENDER_QUESTIONING",
                    "INTERSEX",
                    "MAN",
                    "NON_BINARY",
                    "OTHER",
                    "PANGENDER",
                    "TRANSFEMININE",
                    "TRANSMASCULINE",
                    "TRANS_HUMAN",
                    "TRANS_MAN",
                    "TRANS_NON_BINARY",
                    "TRANS_WOMAN",
                    "TWO_SPIRIT",
                    "WOMAN",
                    "WOMAN_WOMAN_COUPLE",
                    "MAN_MAN_COUPLE",
                    "MAN_WOMAN_COUPLE",
                ],
                "recentlyOnline": None,
                "sexuality": "BISEXUAL",
                "status": "INCOMPLETE",
                "streamToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYzQ3ZjU5MTgtYjZkZS00YjUzLWJiZTQtYjgwOTk4MzMzMjYxIn0.4E-PJ5YzrHRRQ5PBc-pExJMmFqkdnNF9WeJuYEcSqd0",
                "__typename": "Profile",
            }
        },
        "extensions": {"requestId": "d1a90056-720d-4761-b863-592243ee2a05"},
    }

    print(ProfileUpdateResponse.parse_response(payload))

    test = ProfileUpdatePayload(
        gender="test",
        desires=["test"],
        looking_for=["test"],
        sexuality="test",
        imaginary_name="test",
        date_of_birth="test",
        bio="test",
    )
    print(test.get_input_payload())
