from typing import Any

from feeld.models.base import BaseResponse, InnerResponse


class Geocode(InnerResponse):
    city: str | None = None
    country: str | None = None


class LocationData(InnerResponse):
    latitude: float | None = None
    longitude: float | None = None
    geocode: Geocode | None = None


class DeviceLocation(InnerResponse):
    device: LocationData


class Location(InnerResponse):
    core: str | None = None
    current: LocationData | None = None
    teleport: LocationData | None = None


class Profile(InnerResponse):
    id: str | None = None
    location: Location | None = None


class DeviceLocationUpdate(InnerResponse):
    id: str | None = None
    location: DeviceLocation | None = None
    profiles: list[Profile] | None = None


class DeviceLocationUpdateResponse(BaseResponse):
    device_location_update: DeviceLocationUpdate | None = None

    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> "DeviceLocationUpdateResponse | None":
        try:
            return cls(device_location_update=data["data"]["deviceLocationUpdate"])
        except (TypeError, KeyError) as e:
            print(f"Missing key {e}: {data}")
            return None


if __name__ == "__main__":
    data = {
        "data": {
            "deviceLocationUpdate": {
                "id": "account#4522f649-789b-41de-a1c6-193bf4c1fa11",
                "location": {
                    "device": {"latitude": 0, "longitude": 0, "geocode": None, "__typename": "Location"},
                    "__typename": "DeviceLocation",
                },
                "profiles": [
                    {
                        "id": "profile#2db90e29-888b-4d4d-9aad-9675a65fc70c",
                        "location": {
                            "current": None,
                            "teleport": {
                                "latitude": 0,
                                "longitude": 0,
                                "geocode": {"city": "Amsterdam", "country": "NL", "__typename": "Geocode"},
                                "__typename": "Location",
                            },
                            "__typename": "TeleportLocation",
                        },
                        "__typename": "Profile",
                    }
                ],
                "__typename": "Account",
            }
        },
        "extensions": {"requestId": "7d689baf-8672-49f5-9484-37c1b4943233"},
    }

    response = DeviceLocationUpdateResponse.parse_response(data)
    print(response)
