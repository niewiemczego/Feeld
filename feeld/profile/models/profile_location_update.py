from typing import Any

from feeld.models.base import BaseResponse, InnerResponse


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
    device: LocationData | None = None


class ProfileLocationUpdate(InnerResponse):
    id: str | None = None
    location: Location | None = None


class ProfileLocationUpdateResponse(BaseResponse):
    profile_location_update: ProfileLocationUpdate | None = None

    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> "ProfileLocationUpdateResponse | None":
        try:
            return cls(profile_location_update=data["data"]["profileLocationUpdate"])
        except (TypeError, KeyError) as e:
            print(f"Missing key {e}: {data}")
            return None


if __name__ == "__main__":
    data = [
        {
            "data": {
                "profileLocationUpdate": {
                    "id": "profile#2db90e29-888b-4d4d-9aad-9675a65fc70c",
                    "location": {
                        "current": None,
                        "teleport": {
                            "latitude": 0,
                            "longitude": 0,
                            "geocode": {"city": "Chicago", "country": "US", "__typename": "Geocode"},
                            "__typename": "Location",
                        },
                        "__typename": "TeleportLocation",
                    },
                    "__typename": "Profile",
                }
            },
            "extensions": {"requestId": "a5c0dfc1-f529-44e5-9753-088ec8cce8f0"},
        },
        {
            "data": {
                "profileLocationUpdate": {
                    "id": "profile#2db90e29-888b-4d4d-9aad-9675a65fc70c",
                    "location": {
                        "device": {"latitude": 0, "longitude": 0, "geocode": None, "__typename": "Location"},
                        "__typename": "DeviceLocation",
                    },
                    "__typename": "Profile",
                }
            },
            "extensions": {"requestId": "534e47b0-07dd-40f0-b153-e1dcb5818f08"},
        },
        {
            "data": {
                "profileLocationUpdate": {
                    "id": "profile#2db90e29-888b-4d4d-9aad-9675a65fc70c",
                    "location": {"core": "FANTASY_BUNKER", "__typename": "VirtualLocation"},
                    "__typename": "Profile",
                }
            },
            "extensions": {"requestId": "a27f757a-0fcf-4b39-bc46-0b0747346681"},
        },
    ]

    for d in data:
        response = ProfileLocationUpdateResponse.parse_response(d)
        print(response)
