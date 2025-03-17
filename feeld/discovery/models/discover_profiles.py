from datetime import datetime
from typing import Any

from feeld.models.base import BaseResponse, InnerResponse
from feeld.models.desires import DesiresType
from feeld.models.gender import GenderType
from feeld.models.sexuality import SexualityType


class ProfileDistance(InnerResponse):
    km: int
    mi: int


class DeviceLocationData(InnerResponse):
    latitude: float | None = None
    longitude: float | None = None
    geocode: str | None = None


class DeviceLocation(InnerResponse):
    device: DeviceLocationData | None = None


class InteractionStatus(InnerResponse):
    message: str | None = None
    mine: str | None = None
    theirs: str | None = None


class Picture(InnerResponse):
    id: str | None = None
    picture_is_private: bool | None = None
    picture_is_safe: bool | None = None
    picture_status: str | None = None
    picture_type: str | None = None
    picture_url: str | None = None
    public_id: str | None = None


class DiscoverProfileMetadata(InnerResponse):
    source: str | None = None


class Profile(InnerResponse):
    bio: str | None = None
    age: int | None = None
    date_of_birth: datetime | None = None
    distance: ProfileDistance | None = None
    desires: list[DesiresType] | None = None
    gender: GenderType | None = None
    id: str | None = None
    status: str | None = None
    imaginary_name: str | None = None
    interaction_status: InteractionStatus | None = None
    interests: list[str] | None = None
    is_majestic: bool | None = None
    is_verified: bool | None = None
    last_seen: datetime | None = None
    location: DeviceLocation | None = None
    sexuality: SexualityType | None = None
    photos: list[Picture] | None = None
    profile_pairs: list | None = None
    is_uplift: bool | None = None
    metadata: DiscoverProfileMetadata | None = None
    stream_user_id: str | None = None
    analytics_id: str | None = None


class ProfilesBatch(InnerResponse):
    nodes: list[Profile] | None = None
    has_next_batch: bool | None = None
    profile_in_sync: bool | None = None
    feed_generated_at: datetime | None = None
    generated_with_profile_updated_at: datetime | None = None
    feed_size: int | None = None
    feed_capacity: int | None = None


class DiscoverProfilesResponse(BaseResponse):
    discovery: ProfilesBatch | None = None

    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> "DiscoverProfilesResponse | None":
        try:
            return cls(discovery=data["data"]["discovery"])
        except (TypeError, KeyError) as e:
            print(f"Missing key {e}: {data}")
            return None


if __name__ == "__main__":
    data = {
        "data": {
            "discovery": {
                "nodes": [
                    {
                        "bio": None,
                        "age": 25,
                        "dateOfBirth": None,
                        "distance": {"km": 7571, "mi": 4704, "__typename": "ProfileDistance"},
                        "desires": [
                            "MFMF",
                            "MMF",
                            "FFM",
                            "MF",
                            "THREESOME",
                            "OPEN_RELATIONSHIP",
                            "FUN",
                            "FRIENDSHIPS",
                            "CONNECTION",
                            "DATES",
                        ],
                        "gender": "MAN",
                        "id": "profile#0069fd6a-ed6f-47e0-9efb-20c466659865",
                        "status": "ACTIVE",
                        "imaginaryName": "Sssam",
                        "interactionStatus": {
                            "message": None,
                            "mine": "NONE",
                            "theirs": "NONE",
                            "__typename": "InteractionStatusBetweenProfilesOutput",
                        },
                        "interests": [],
                        "isMajestic": True,
                        "isVerified": False,
                        "lastSeen": "2024-09-05T16:50:53.517Z",
                        "location": {
                            "device": {"latitude": 0, "longitude": 0, "geocode": None, "__typename": "Location"},
                            "__typename": "DeviceLocation",
                        },
                        "sexuality": "STRAIGHT",
                        "photos": [
                            {
                                "id": "picture|profile#0069fd6a-ed6f-47e0-9efb-20c466659865-599059ab-1ee0-4580-abec-c845ffc00770",
                                "pictureIsPrivate": False,
                                "pictureIsSafe": True,
                                "pictureStatus": "READY",
                                "pictureType": "DEFAULT",
                                "pictureUrl": "https://res.cloudinary.com/threender/image/upload/v1725494203/85d2f28c-6869-4975-8566-c09715ce0093.jpg",
                                "publicId": "85d2f28c-6869-4975-8566-c09715ce0093",
                                "__typename": "Picture",
                            }
                        ],
                        "profilePairs": [],
                        "isUplift": True,
                        "__typename": "Profile",
                        "metadata": {"source": "UPLIFT", "__typename": "DiscoverProfileMetadata"},
                        "streamUserId": "00ed528c-5607-470a-bfff-a0d326bcc969",
                        "analyticsId": "00ed528c-5607-470a-bfff-a0d326bcc969",
                    }
                ],
                "hasNextBatch": True,
                "profileInSync": False,
                "feedGeneratedAt": "2024-09-05T17:00:26.005Z",
                "generatedWithProfileUpdatedAt": "2024-09-05T16:59:20.117Z",
                "feedSize": 200,
                "feedCapacity": 200,
                "__typename": "ProfilesBatch",
            }
        },
        "extensions": {"requestId": "7e77c0a0-e433-4f9b-9b99-59fcebf3694a"},
    }

    response = DiscoverProfilesResponse.parse_response(data)
    print(response)
