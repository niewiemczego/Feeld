import logging

from feeld.chat import ChatManager
from feeld.models import AnalyticsResponse, DeviceLocationUpdateResponse
from feeld.networking.http_manager import HTTPManager
from feeld.networking.proxy_manager import ProxyManager
from feeld.profile import ProfileManager


class APIManager:
    _logger = logging.getLogger(__name__)

    def __init__(self, proxy_manager: ProxyManager | None = None) -> None:
        self._http_manager = HTTPManager(proxy_manager)
        self.chat_manager = ChatManager(self._http_manager)
        self.profile_manager = ProfileManager(self._http_manager)

    async def update_device_location(self, latitude: float, longitude: float) -> DeviceLocationUpdateResponse | None:
        payload = {
            "operationName": "DeviceLocationUpdate",
            "variables": {"input": {"latitude": round(latitude, 3), "longitude": round(longitude, 3)}},
            "query": "mutation DeviceLocationUpdate($input: DeviceLocationInput!) {\n  deviceLocationUpdate(input: $input) {\n    id\n    location {\n      device {\n        latitude\n        longitude\n        geocode {\n          city\n          country\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    profiles {\n      id\n      location {\n        ...ProfileLocationFragment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ProfileLocationFragment on ProfileLocation {\n  ... on DeviceLocation {\n    device {\n      latitude\n      longitude\n      geocode {\n        city\n        country\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ... on VirtualLocation {\n    core\n    __typename\n  }\n  ... on TeleportLocation {\n    current: device {\n      city\n      country\n      __typename\n    }\n    teleport {\n      latitude\n      longitude\n      geocode {\n        city\n        country\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}",
        }

        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return None

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to update device location - Unknown error[{res.status_code}]")
            return None

        return DeviceLocationUpdateResponse.parse_response(res.json())

    async def update_last_seen_status(self) -> bool:
        payload = {
            "operationName": "LastSeenProviderUpdateProfile",
            "variables": {"profileId": self._http_manager.profile_id},
            "query": "mutation LastSeenProviderUpdateProfile($profileId: String!) {\n  updatedProfileLastSeen: profileUpdateLastSeen(profileId: $profileId)\n}",
        }
        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return False

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to update last seen status - Unknown error[{res.status_code}]")
            return False

        return True

    async def get_analytics_data(self, profile_id: str) -> AnalyticsResponse | None:
        payload = {
            "operationName": "AnalyticsQuery",
            "variables": {"profileId": profile_id},
            "query": "query AnalyticsQuery($profileId: String!) {\n  account {\n    ...AnalyticsAccountFragment\n    __typename\n  }\n  profile(id: $profileId) {\n    ...AnalyticsOwnProfileFragment\n    __typename\n  }\n}\n\nfragment AnalyticsAccountFragment on Account {\n  id\n  analyticsId\n  __typename\n}\n\nfragment AnalyticsOwnProfileFragment on Profile {\n  id\n  age\n  ageRange\n  desires\n  desiringFor\n  analyticsId\n  distanceMax\n  isUplift\n  recentlyOnline\n  isIncognito\n  status\n  isMajestic\n  gender\n  dateOfBirth\n  lookingFor\n  sexuality\n  allowPWM\n  location {\n    ...ProfileLocationFragment\n    __typename\n  }\n  profilePairs {\n    identityId\n    __typename\n  }\n  __typename\n}\n\nfragment ProfileLocationFragment on ProfileLocation {\n  ... on DeviceLocation {\n    device {\n      latitude\n      longitude\n      geocode {\n        city\n        country\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ... on VirtualLocation {\n    core\n    __typename\n  }\n  ... on TeleportLocation {\n    current: device {\n      city\n      country\n      __typename\n    }\n    teleport {\n      latitude\n      longitude\n      geocode {\n        city\n        country\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}",
        }
        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return None

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to get analytics data - Unknown error[{res.status_code}]")
            return None

        return AnalyticsResponse.parse_response(res.json())

    async def terminate_account(self) -> bool:
        payload = {
            "operationName": "AccountTerminate",
            "variables": {},
            "query": "mutation AccountTerminate {\n  accountTerminate {\n    email\n    status\n    __typename\n  }\n}",
        }
        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return False

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to terminate account - Unknown error[{res.status_code}]")
            return False

        return True
