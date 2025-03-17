import logging
from typing import Any

from feeld.models import AuthProviderResponse, PopularLocation, PopularLocations
from feeld.networking.http_manager import HTTPManager
from feeld.profile.models.profile_location_update import ProfileLocationUpdateResponse
from feeld.profile.models.profile_update import ProfileUpdatePayload, ProfileUpdateResponse


class ProfileManager:
    _logger = logging.getLogger(__name__)

    def __init__(self, http_manager: HTTPManager):
        self._http_manager = http_manager

    async def get_profile_data(self) -> AuthProviderResponse | None:
        payload = {
            "operationName": "AuthProviderQuery",
            "variables": {},
            "query": "query AuthProviderQuery {\n  account {\n    ...AuthProviderFragment\n    __typename\n  }\n}\n\nfragment AuthProviderFragment on Account {\n  id\n  email\n  analyticsId\n  status\n  isFinishedOnboarding\n  isMajestic\n  upliftExpirationTimestamp\n  isUplift\n  isDistanceInMiles\n  language\n  location {\n    device {\n      country\n      __typename\n    }\n    __typename\n  }\n  profiles {\n    ...AuthProfile\n    __typename\n  }\n  __typename\n}\n\nfragment AuthProfile on Profile {\n  ...ChatUser\n  ...AnalyticsOwnProfileFragment\n  ...ProfilePairsFragment\n  imaginaryName\n  photos {\n    pictureUrl\n    pictureUrl\n    pictureStatus\n    __typename\n  }\n  __typename\n}\n\nfragment ChatUser on Profile {\n  id\n  streamToken\n  streamUserId\n  __typename\n}\n\nfragment AnalyticsOwnProfileFragment on Profile {\n  id\n  age\n  ageRange\n  desires\n  desiringFor\n  analyticsId\n  distanceMax\n  isUplift\n  recentlyOnline\n  isIncognito\n  status\n  isMajestic\n  gender\n  dateOfBirth\n  lookingFor\n  sexuality\n  allowPWM\n  location {\n    ...ProfileLocationFragment\n    __typename\n  }\n  profilePairs {\n    identityId\n    __typename\n  }\n  __typename\n}\n\nfragment ProfileLocationFragment on ProfileLocation {\n  ... on DeviceLocation {\n    device {\n      latitude\n      longitude\n      geocode {\n        city\n        country\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ... on VirtualLocation {\n    core\n    __typename\n  }\n  ... on TeleportLocation {\n    current: device {\n      city\n      country\n      __typename\n    }\n    teleport {\n      latitude\n      longitude\n      geocode {\n        city\n        country\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ProfilePairsFragment on Profile {\n  id\n  pairCount\n  profilePairs {\n    identityId\n    createdAt\n    partnerLabel\n    otherProfile {\n      id\n      age\n      imaginaryName\n      dateOfBirth\n      gender\n      sexuality\n      isIncognito\n      photos {\n        ...GetPictureUrlFragment\n        __typename\n      }\n      ...ProfileInteractionStatusFragment\n      status\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment GetPictureUrlFragment on Picture {\n  id\n  publicId\n  pictureIsSafe\n  pictureIsPrivate\n  pictureUrl\n  __typename\n}\n\nfragment ProfileInteractionStatusFragment on Profile {\n  interactionStatus {\n    message\n    mine\n    theirs\n    __typename\n  }\n  __typename\n}",
        }

        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, headers=self._http_manager._default_headers, json=payload
        )
        if res is None:
            return None

        self._logger.info(res.text)
        self._logger.info(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to get profile data - Unknown error[{res.status_code}]")
            return None

        return AuthProviderResponse.parse_response(res.json())

    async def update_profile_location(
        self,
        latitude: float | None = None,
        longitude: float | None = None,
        popular_location: PopularLocation | None = None,
    ) -> ProfileLocationUpdateResponse | None:
        if not latitude and not longitude and not popular_location:
            self._logger.error("Failed to update profile location - No location provided")
            return None

        if latitude and longitude:
            data = {"deviceLocation": {"latitude": round(latitude, 3), "longitude": round(longitude, 3)}}

        if popular_location in [
            PopularLocations.STAYING_AT_HOME.value,
            PopularLocations.REMOTE_TRIOS.value,
            PopularLocations.FANTASY.value,
        ]:
            data = {"virtualLocation": {"core": popular_location.city}}
        else:
            data = {
                "teleportLocation": {
                    "city": popular_location.city,
                    "country": popular_location.country,
                    "latitude": round(popular_location.latitude, 3),
                    "longitude": round(popular_location.longitude, 3),
                }
            }

        payload = {
            "operationName": "ProfileLocationUpdate",
            "variables": {"input": data},
            "query": "mutation ProfileLocationUpdate($input: ProfileLocationInput!) {\n  profileLocationUpdate(input: $input) {\n    id\n    location {\n      ...ProfileLocationFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ProfileLocationFragment on ProfileLocation {\n  ... on DeviceLocation {\n    device {\n      latitude\n      longitude\n      geocode {\n        city\n        country\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ... on VirtualLocation {\n    core\n    __typename\n  }\n  ... on TeleportLocation {\n    current: device {\n      city\n      country\n      __typename\n    }\n    teleport {\n      latitude\n      longitude\n      geocode {\n        city\n        country\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}",
        }

        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return None

        self._logger.info(res.text)
        self._logger.info(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to update profile location - Unknown error[{res.status_code}]")
            return None

        return ProfileLocationUpdateResponse.parse_response(res.json())

    async def update_profile(self, profile_payload: ProfileUpdatePayload) -> dict[str, Any] | None:
        payload = {
            "operationName": "ProfileUpdate",
            "variables": {"input": profile_payload.get_input_payload()},
            "query": "mutation ProfileUpdate($input: ProfileUpdateInput!) {\n  profileUpdate(input: $input) {\n    id\n    age\n    ageRange\n    allowPWM\n    bio\n    completionStatus\n    dateOfBirth\n    desires\n    distanceMax\n    gender\n    imaginaryName\n    interests\n    isIncognito\n    lookingFor\n    recentlyOnline\n    sexuality\n    status\n    streamToken\n    __typename\n  }\n}",
        }

        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return None

        self._logger.info(res.text)
        self._logger.info(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to update profile - Unknown error[{res.status_code}]")
            return None

        return ProfileUpdateResponse.parse_response(res.json())
