from datetime import datetime
from typing import Any

from pydantic import Field

from feeld.models.base import BaseResponse, InnerResponse
from feeld.models.desires import DesiresType
from feeld.models.gender import GenderType
from feeld.models.looking_for import LookingForType
from feeld.models.sexuality import SexualityType


class DeviceLocationData(InnerResponse):
    country: str | None = None


class DeviceLocation(InnerResponse):
    device: DeviceLocationData | None = None


class Picture(InnerResponse):
    picture_url: str | None = None
    picture_status: str | None = None


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
    stream_token: str | None = None
    stream_user_id: str | None = None
    age: int | None = None
    age_range: list[int | None] | None = None
    desires: list[DesiresType] | None = None
    desiring_for: str | list | None = None
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
    pair_count: int | None = None
    imaginary_name: str | None = None
    photos: list[Picture] | None = None


class Account(InnerResponse):
    id: str | None = None
    email: str | None = None
    analytics_id: str | None = None
    status: str | None = None
    is_finished_onboarding: bool | None = None
    is_majestic: bool | None = None
    uplift_expiration_timestamp: str | datetime | None = None
    is_uplift: bool | None = None
    is_distance_in_miles: bool | None = None
    language: str | None = None
    location: DeviceLocation | None = None
    profiles: list[Profile] | None = None


class AuthProviderResponse(BaseResponse):
    account: Account | None = None

    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> "AuthProviderResponse | None":
        try:
            return cls(account=data["data"]["account"])
        except (TypeError, KeyError) as e:
            print(f"Missing key {e}: {data}")
            return None


if __name__ == "__main__":
    data = {
        "data": {
            "account": {
                "id": "account#4522f649-789b-41de-a1c6-193bf4c1fa11",
                "email": "simmon.buisness@gmail.com",
                "analyticsId": "35eff02e-bd0e-4c9f-9894-fd5a02d918ae",
                "status": "ACTIVE",
                "isFinishedOnboarding": True,
                "isMajestic": False,
                "upliftExpirationTimestamp": None,
                "isUplift": False,
                "isDistanceInMiles": False,
                "language": "en",
                "location": {"device": {"country": "PL", "__typename": "Location"}, "__typename": "DeviceLocation"},
                "profiles": [
                    {
                        "id": "profile#2db90e29-888b-4d4d-9aad-9675a65fc70c",
                        "streamToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNDUzNDBmNzItNjgyYS00MDZhLTk5N2ItYjY3ZGY5OTBkYzhmIn0.N7wMAayH38iRwAu3_aulfsFN3xXp-4LIykI0hLKILdU",
                        "streamUserId": "45340f72-682a-406a-997b-b67df990dc8f",
                        "__typename": "Profile",
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
                        "analyticsId": "45340f72-682a-406a-997b-b67df990dc8f",
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
                        "pairCount": 0,
                        "imaginaryName": "Jagoda",
                        "photos": [
                            {
                                "pictureUrl": "https://res.cloudinary.com/threender/image/upload/v1725404430/992d03ad-fd88-488a-8223-c506e9378497.jpg",
                                "pictureStatus": "READY",
                                "__typename": "Picture",
                            },
                            {
                                "pictureUrl": "https://res.cloudinary.com/threender/image/upload/v1725404431/55464a99-c215-43fb-b57f-5ad2c59c4821.jpg",
                                "pictureStatus": "READY",
                                "__typename": "Picture",
                            },
                            {
                                "pictureUrl": "https://res.cloudinary.com/threender/image/upload/v1725404432/7cfb16fe-3612-44de-a886-5af8d75648e7.jpg",
                                "pictureStatus": "READY",
                                "__typename": "Picture",
                            },
                            {
                                "pictureUrl": "https://res.cloudinary.com/threender/image/upload/v1725404433/6a8939aa-5b04-4cf2-97d3-8328114664e8.jpg",
                                "pictureStatus": "READY",
                                "__typename": "Picture",
                            },
                        ],
                    }
                ],
                "__typename": "Account",
            }
        },
        "extensions": {"requestId": "eb54cdc5-ab75-407b-841c-64d721dac083"},
    }

    response = AuthProviderResponse.parse_response(data)
    print(response)
