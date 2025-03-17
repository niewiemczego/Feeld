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


class WhoLikesMeResponse(BaseResponse):
    interactions: PaginatedProfiles | None = None

    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> "WhoLikesMeResponse | None":
        try:
            return cls(interactions=data["data"]["interactions"])
        except (KeyError, TypeError) as e:
            print(f"Error {e}: {data}")
            return None


if __name__ == "__main__":
    data = {
        "data": {
            "interactions": {
                "nodes": [
                    {
                        "id": "profile#e5f32714-8847-483c-ad17-f5cc76420480",
                        "age": 34,
                        "gender": "MAN",
                        "status": "ACTIVE",
                        "lastSeen": "2024-09-05T10:41:53.846Z",
                        "isUplift": False,
                        "sexuality": "STRAIGHT",
                        "isMajestic": True,
                        "isVerified": False,
                        "dateOfBirth": None,
                        "streamUserId": "7d8ba02d-7937-440d-94d3-fb2bc77843c1",
                        "imaginaryName": "Mr Casual",
                        "interactionStatus": {
                            "message": None,
                            "mine": "NONE",
                            "theirs": "LIKED",
                            "__typename": "InteractionStatusBetweenProfilesOutput",
                        },
                        "profilePairs": [],
                        "distance": None,
                        "location": {"core": "FANTASY_BUNKER", "__typename": "VirtualLocation"},
                        "photos": [
                            {
                                "id": "picture|profile#e5f32714-8847-483c-ad17-f5cc76420480-525058b9-77f9-410e-ab79-5fcc8bdedcb5",
                                "pictureIsPrivate": False,
                                "pictureIsSafe": True,
                                "pictureStatus": "READY",
                                "pictureType": "DEFAULT",
                                "pictureUrl": "https://res.cloudinary.com/threender/image/upload/v1724850464/9aaebd5c-fb48-4b34-a6dc-bc52237c2e43.jpg",
                                "publicId": "9aaebd5c-fb48-4b34-a6dc-bc52237c2e43",
                                "__typename": "Picture",
                            },
                            {
                                "id": "HIDDEN-2",
                                "pictureIsPrivate": True,
                                "pictureIsSafe": True,
                                "pictureStatus": "READY",
                                "pictureType": "SECONDARY",
                                "pictureUrl": "HIDDEN",
                                "publicId": "HIDDEN",
                                "__typename": "Picture",
                            },
                            {
                                "id": "HIDDEN-3",
                                "pictureIsPrivate": True,
                                "pictureIsSafe": True,
                                "pictureStatus": "READY",
                                "pictureType": "SECONDARY",
                                "pictureUrl": "HIDDEN",
                                "publicId": "HIDDEN",
                                "__typename": "Picture",
                            },
                            {
                                "id": "HIDDEN-4",
                                "pictureIsPrivate": True,
                                "pictureIsSafe": True,
                                "pictureStatus": "READY",
                                "pictureType": "SECONDARY",
                                "pictureUrl": "HIDDEN",
                                "publicId": "HIDDEN",
                                "__typename": "Picture",
                            },
                        ],
                        "__typename": "Profile",
                    }
                ],
                "pageInfo": {"total": 620, "hasNextPage": False, "nextPageCursor": None, "__typename": "PageInfo"},
                "__typename": "PaginatedProfiles",
            }
        },
        "extensions": {"requestId": "6031c809-0e07-4d67-b7e7-5fdb06e32564"},
    }

    response = WhoLikesMeResponse.parse_response(data)
    print(response)
