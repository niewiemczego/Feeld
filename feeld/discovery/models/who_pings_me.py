from datetime import datetime
from typing import Any

from feeld.models import GenderType, SexualityType
from feeld.models.base import BaseResponse, InnerResponse


class Picture(InnerResponse):
    id: str | None = None
    picture_is_private: bool | None = None
    picture_is_safe: bool | None = None
    picture_status: str | None = None
    picture_type: str | None = None
    picture_url: str | None = None
    public_id: str | None = None


class ProfilePair(InnerResponse):
    identity_id: str | None = None


class InteractionStatus(InnerResponse):
    message: str | None = None
    mine: str | None = None
    theirs: str | None = None


class ProfileDistance(InnerResponse):
    km: int | None = None
    mi: int | None = None


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
    gender: GenderType | None = None
    status: str | None = None
    last_seen: datetime | None = None
    is_uplift: bool | None = None
    sexuality: SexualityType | None = None
    is_majestic: bool | None = None
    is_verified: bool | None = None
    date_of_birth: str | None | None = None
    stream_user_id: str | None = None
    imaginary_name: str | None = None
    interaction_status: InteractionStatus | None = None
    profile_pairs: list[ProfilePair] | None = None
    distance: ProfileDistance | None = None
    location: Location | None = None
    photos: list[Picture] | None = None


class PageInfo(InnerResponse):
    total: int | None = None
    has_next_page: bool | None = None
    next_page_cursor: str | None = None


class PaginatedProfiles(InnerResponse):
    nodes: list[Profile] | None = None
    page_info: PageInfo | None = None


class WhoPingsMeResponse(BaseResponse):
    interactions: PaginatedProfiles | None = None

    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> "WhoPingsMeResponse | None":
        try:
            return cls(interactions=data["data"]["interactions"])
        except (TypeError, KeyError) as e:
            print(f"Missing key {e}: {data}")
            return None


if __name__ == "__main__":
    data = {
        "data": {
            "interactions": {
                "nodes": [
                    {
                        "id": "profile#92ab07fc-06fa-52fc-a995-e8abbde66835",
                        "age": 40,
                        "gender": "MAN",
                        "status": "ACTIVE",
                        "lastSeen": "2024-09-05T09:34:32.911Z",
                        "isUplift": False,
                        "sexuality": "STRAIGHT",
                        "isMajestic": True,
                        "isVerified": False,
                        "dateOfBirth": None,
                        "streamUserId": "6116bbe8aa9469004300009e",
                        "imaginaryName": "ATraveler",
                        "interactionStatus": {
                            "message": None,
                            "mine": "NONE",
                            "theirs": "PINGED",
                            "__typename": "InteractionStatusBetweenProfilesOutput",
                        },
                        "profilePairs": [
                            {
                                "identityId": "pair|profile#92ab07fc-06fa-52fc-a995-e8abbde66835|profile#95b89a86-de2a-5967-939f-2a22f15f74de",
                                "__typename": "ProfilePair",
                            }
                        ],
                        "distance": None,
                        "location": {"core": "FANTASY_BUNKER", "__typename": "VirtualLocation"},
                        "photos": [
                            {
                                "id": "picture|profile#92ab07fc-06fa-52fc-a995-e8abbde66835-869a53a6-dfe0-5824-81c5-ae4c0c7578e0",
                                "pictureIsPrivate": False,
                                "pictureIsSafe": True,
                                "pictureStatus": "READY",
                                "pictureType": "DEFAULT",
                                "pictureUrl": "https://res.cloudinary.com/threender/image/upload/v1628880818/c7bbb52a-944d-4f96-8778-6b25862ae94f.jpg",
                                "publicId": "c7bbb52a-944d-4f96-8778-6b25862ae94f",
                                "__typename": "Picture",
                            },
                            {
                                "id": "picture|profile#92ab07fc-06fa-52fc-a995-e8abbde66835-581422e6-3cc1-5bab-a3f6-35347fe89b5d",
                                "pictureIsPrivate": False,
                                "pictureIsSafe": True,
                                "pictureStatus": "READY",
                                "pictureType": "SECONDARY",
                                "pictureUrl": "https://res.cloudinary.com/threender/image/upload/v1664797881/6c8e848c-4ee5-4f1f-85fe-af00211853f6.jpg",
                                "publicId": "6c8e848c-4ee5-4f1f-85fe-af00211853f6",
                                "__typename": "Picture",
                            },
                        ],
                        "__typename": "Profile",
                    },
                ],
                "pageInfo": {"total": 9, "hasNextPage": False, "nextPageCursor": None, "__typename": "PageInfo"},
                "__typename": "PaginatedProfiles",
            }
        },
        "extensions": {"requestId": "a99d1af4-5869-4d66-af8b-97a491b65d30"},
    }

    response = WhoPingsMeResponse.parse_response(data)
    print(response)
