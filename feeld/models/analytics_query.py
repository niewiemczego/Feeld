from datetime import datetime
from typing import Any

from pydantic import Field

from feeld.models.base import BaseResponse, InnerResponse
from feeld.models.desires import DesiresType
from feeld.models.gender import GenderType
from feeld.models.looking_for import LookingForType
from feeld.models.sexuality import SexualityType


class Account(InnerResponse):
    id: str | None = None
    analytics_id: str | None = None


class Geocode(InnerResponse):
    city: str | None = None
    country: str | None = None


class LocationData(InnerResponse):
    latitude: float | None = None
    longitude: float | None = None
    geocode: Geocode | None = None


class Location(InnerResponse):
    core: str | None = None
    current: LocationData | None = None
    teleport: LocationData | None = None


class Profile(InnerResponse):
    id: str | None = None
    age: int | None = None
    age_range: list[int | None] | None = None
    desires: list[DesiresType] | None = None
    desiring_for: str | None = None
    analytics_id: str | None = None
    distance_max: int | None = None
    is_uplift: bool | None = None
    recently_online: bool | None = None
    is_incognito: bool | None = None
    status: str | None = None
    is_majestic: bool | None = None
    gender: GenderType | None = None
    date_of_birth: datetime | None = None
    looking_for: list[LookingForType] | None = None
    sexuality: SexualityType | None = None
    allow_pwm: bool | None = Field(default=None, alias="allowPWM")
    location: Location | None = None
    profile_pairs: list | None = None


class AnalyticsResponse(BaseResponse):
    account: Account | None = None
    profile: Profile | None = None

    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> "AnalyticsResponse | None":
        try:
            return cls(account=data["data"]["account"], profile=data["data"]["profile"])
        except (TypeError, KeyError) as e:
            print(f"Missing key {e}: {data}")
            return None


if __name__ == "__main__":
    data = {
        "data": {
            "account": {
                "id": "account#4112f649-879g-41de-a1c6-132bf5c1fa21",
                "analyticsId": "35efaO2e-bd0e-4c9f-9894-f14a02dv18ae",
                "__typename": "Account",
            },
            "profile": {
                "id": "profile#2db90e29-888b-4d4d-9aad-9675a65fc70c",
                "age": 21,
                "ageRange": [18, None],
                "desires": [
                    "FWB",
                    "FUN",
                    "FRIENDSHIPS",
                    "OPEN_RELATIONSHIP",
                    "COUPLES",
                    "SINGLES",
                    "SUBMISSIVES",
                    "CUDDLING",
                    "GROUP",
                    "THREESOME",
                ],
                "desiringFor": None,
                "analyticsId": "45230f72-612c-406a-857b-b67df990dc8f",
                "distanceMax": 400,
                "isUplift": False,
                "recentlyOnline": None,
                "isIncognito": False,
                "status": "ACTIVE",
                "isMajestic": False,
                "gender": "WOMAN",
                "dateOfBirth": "2003-01-01T00:00:00.000Z",
                "lookingFor": [
                    "MAN",
                    "WOMAN",
                    "MAN_WOMAN_COUPLE",
                    "MAN_MAN_COUPLE",
                    "WOMAN_WOMAN_COUPLE",
                    "AGENDER",
                    "ANDROGYNOUS",
                    "BIGENDER",
                    "GENDER_FLUID",
                    "GENDER_NONCONFORMING",
                    "TRANS_WOMAN",
                    "TRANS_NON_BINARY",
                    "TRANS_MAN",
                    "TRANS_HUMAN",
                    "TRANSMASCULINE",
                    "TRANSFEMININE",
                    "PANGENDER",
                    "OTHER",
                    "NON_BINARY",
                    "INTERSEX",
                    "GENDER_QUESTIONING",
                    "GENDER_QUEER",
                    "TWO_SPIRIT",
                ],
                "sexuality": "HETEROFLEXIBLE",
                "allowPWM": True,
                "location": {"core": "FANTASY_BUNKER", "__typename": "VirtualLocation"},
                "profilePairs": [],
                "__typename": "Profile",
            },
        },
        "extensions": {"requestId": "29y27e78-9d60-49a9-926e-71022f8aa5e7"},
    }
    response = AnalyticsResponse.parse_response(data)
    print(response)
