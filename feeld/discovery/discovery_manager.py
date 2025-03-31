import logging
from typing import Literal

from feeld.discovery.models.device_location_update import DeviceLocationUpdateResponse
from feeld.discovery.models.discover_profiles import DiscoverProfilesResponse
from feeld.discovery.models.head_summaries import HeadSummariesResponse
from feeld.discovery.models.who_likes_me import WhoLikesMeResponse
from feeld.discovery.models.who_pings_me import WhoPingsMeResponse
from feeld.models.desires import DesiresType
from feeld.models.looking_for import LookingForType
from feeld.networking.http_manager import HTTPManager


class DiscoveryManager:
    _logger = logging.getLogger(__name__)

    def __init__(self, http_manager: HTTPManager) -> None:
        self._http_manager = http_manager

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

    async def update_search_settings(
        self,
        age_range: list[int | None] | None = None,
        distance_max_km: int | None = None,
        looking_for: list[LookingForType] | None = None,
        recently_online: bool = False,
        desiring_for: list[DesiresType] | None = None,
    ) -> bool:
        """
        :param age_range: Age range to filter users by. i.e: [18, 45], [30, None], [18, None]. There must be always value for the minimum age, maximum age is 99
        :param max_distance: Maximum distance in km to filter users by. Min value is 5, max value is 400
        :param looking_for: List of looking for types to filter users by
        :param recently_online: Filter users by recently online. Requires majestic membership
        :param desiring_for: List of desires to filter users by. Requires majestic membership
        """
        settings_data = {"recentlyOnline": recently_online, "desiringFor": [] if desiring_for is None else desiring_for}

        if age_range is not None:
            settings_data["ageRange"] = age_range

        if distance_max_km is not None:
            settings_data["distanceMax"] = distance_max_km

        if looking_for is not None:
            settings_data["lookingFor"] = looking_for

        payload = {
            "operationName": "SearchSettingsUpdate",
            "variables": settings_data,
            "query": "mutation SearchSettingsUpdate($ageRange: [Int], $distanceMax: Float, $desiringFor: [Desire!], $lookingFor: [LookingFor!], $recentlyOnline: Boolean) {\n  profileUpdate(\n    input: {ageRange: $ageRange, distanceMax: $distanceMax, desiringFor: $desiringFor, lookingFor: $lookingFor, recentlyOnline: $recentlyOnline}\n  ) {\n    ...SearchSettingsProfileFragment\n    __typename\n  }\n}\n\nfragment SearchSettingsProfileFragment on Profile {\n  id\n  ageRange\n  distanceMax\n  desiringFor\n  lookingFor\n  location {\n    ...ProfileLocationFragment\n    __typename\n  }\n  recentlyOnline\n  __typename\n}\n\nfragment ProfileLocationFragment on ProfileLocation {\n  ... on DeviceLocation {\n    device {\n      latitude\n      longitude\n      geocode {\n        city\n        country\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ... on VirtualLocation {\n    core\n    __typename\n  }\n  ... on TeleportLocation {\n    current: device {\n      city\n      country\n      __typename\n    }\n    teleport {\n      latitude\n      longitude\n      geocode {\n        city\n        country\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}",
        }

        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return False

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200:
            self._logger.error(f"Failed to update search settings - Unknown error[{res.status_code}]")
            return False

        return True

    async def get_users_to_swipe_on(
        self,
        age_range: list[int | None],
        max_distance: int = 400,
        recently_online: bool = False,
        already_shown_profile_ids: list[str] | None = None,
    ) -> DiscoverProfilesResponse | None:
        """
        Get users data to swipe on based on the provided filters
        :param age_range: Age range to filter users by. i.e: [18, 45], [30, None], [18, None]. There must be always value for the minimum age, maximum age is 99
        :param max_distance: Maximum distance in km to filter users by. Min value is 5, max value is 400
        :param recently_online: Filter users by recently online
        :param already_shown_profile_ids: List of profile IDs that you don't want to see again
        """
        payload = {
            "operationName": "DiscoverProfiles",
            "variables": {
                "input": {
                    "filters": {
                        "ageRange": age_range,
                        "maxDistance": max_distance,
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
                        "recentlyOnline": recently_online,
                    }
                }
            },
            "query": "query DiscoverProfiles($input: ProfileDiscoveryInput!) {\n  discovery(input: $input) {\n    nodes {\n      ...DiscoveryProfileFragment\n      __typename\n    }\n    hasNextBatch\n    profileInSync\n    feedGeneratedAt\n    generatedWithProfileUpdatedAt\n    feedSize\n    feedCapacity\n    __typename\n  }\n}\n\nfragment DiscoveryProfileFragment on Profile {\n  ...ProfileContentProfileFragment\n  ...DiscoveryAnalyticsMetadata\n  streamUserId\n  analyticsId\n  age\n  distance {\n    km\n    mi\n    __typename\n  }\n  __typename\n}\n\nfragment ProfileContentProfileFragment on Profile {\n  bio\n  age\n  dateOfBirth\n  distance {\n    km\n    mi\n    __typename\n  }\n  desires\n  gender\n  id\n  status\n  imaginaryName\n  interactionStatus {\n    message\n    mine\n    theirs\n    __typename\n  }\n  interests\n  isMajestic\n  isVerified\n  lastSeen\n  location {\n    ...ProfileLocationFragment\n    __typename\n  }\n  sexuality\n  photos {\n    ...PhotoCarouselPictureFragment\n    __typename\n  }\n  profilePairs {\n    createdAt\n    __typename\n  }\n  ...AnalyticsProfileFragment\n  __typename\n}\n\nfragment ProfileLocationFragment on ProfileLocation {\n  ... on DeviceLocation {\n    device {\n      latitude\n      longitude\n      geocode {\n        city\n        country\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ... on VirtualLocation {\n    core\n    __typename\n  }\n  ... on TeleportLocation {\n    current: device {\n      city\n      country\n      __typename\n    }\n    teleport {\n      latitude\n      longitude\n      geocode {\n        city\n        country\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PhotoCarouselPictureFragment on Picture {\n  id\n  pictureIsPrivate\n  pictureIsSafe\n  pictureStatus\n  pictureType\n  pictureUrl\n  publicId\n  __typename\n}\n\nfragment AnalyticsProfileFragment on Profile {\n  id\n  isUplift\n  lastSeen\n  age\n  gender\n  sexuality\n  distance {\n    km\n    mi\n    __typename\n  }\n  profilePairs {\n    identityId\n    __typename\n  }\n  __typename\n}\n\nfragment DiscoveryAnalyticsMetadata on Profile {\n  metadata {\n    source\n    __typename\n  }\n  __typename\n}",
        }

        if already_shown_profile_ids is not None:
            payload["variables"]["input"]["filters"]["alreadyShownProfileIDs"] = already_shown_profile_ids

        res = await self._http_manager._request(
            "POST",
            self._http_manager._BASE_API_URL,
            self._http_manager._default_headers,
            json=payload,
        )
        if res is None:
            return None

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to swipe on users - Unknown error[{res.status_code}]")
            return None

        return DiscoverProfilesResponse.parse_response(res.json())

    async def get_matches(self, limit: int = 10, next_page_cursor: str | None = None) -> HeadSummariesResponse | None:
        payload = {
            "operationName": "HeaderSummaries",
            "variables": {"limit": limit} if next_page_cursor is None else {"limit": limit, "cursor": next_page_cursor},
            "query": "query HeaderSummaries($limit: Int = "
            + str(limit)
            + ", $cursor: String) {\n  summaries: getChatSummariesForChatHeader(limit: $limit, cursor: $cursor) {\n    nodes {\n      ...ChatSummary\n      __typename\n    }\n    pageInfo {\n      hasNextPage\n      nextPageCursor\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ChatSummary on ChatSummary {\n  ...ChatSummaryItem\n  __typename\n}\n\nfragment ChatSummaryItem on ChatSummary {\n  id\n  name\n  type\n  status\n  avatarSet\n  memberCount\n  latestMessage\n  streamChannelId\n  targetProfileId\n  enableChatContentModeration\n  __typename\n}",
        }
        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return None

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to get matches - Unknown error[{res.status_code}]")
            return None

        return HeadSummariesResponse.parse_response(res.json())

    async def get_likes(
        self,
        sort_by: Literal["LAST_INTERACTION", "LAST_ONLINE", "DISTANCE"] = "LAST_INTERACTION",
        next_page_cursor: str | None = None,
    ) -> WhoLikesMeResponse | None:
        """
        Get users who liked you

        :param sort_by: Sort users by last interaction, last online or distance. Requires majestic membership to be able to sort by other than 'LAST_INTERACTION'
        """
        payload = {
            "operationName": "WhoLikesMe",
            "variables": {"sortBy": sort_by}
            if next_page_cursor is None
            else {"sortBy": sort_by, "cursor": next_page_cursor},
            "query": "query WhoLikesMe($limit: Int, $cursor: String, $sortBy: SortBy!) {\n  interactions: whoLikesMe(\n    input: {sortBy: $sortBy}\n    limit: $limit\n    cursor: $cursor\n  ) {\n    nodes {\n      ...LikesProfileFragment\n      __typename\n    }\n    pageInfo {\n      total\n      hasNextPage\n      nextPageCursor\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment LikesProfileFragment on Profile {\n  id\n  age\n  gender\n  status\n  lastSeen\n  isUplift\n  sexuality\n  isMajestic\n  isVerified\n  dateOfBirth\n  streamUserId\n  imaginaryName\n  interactionStatus {\n    message\n    mine\n    theirs\n    __typename\n  }\n  profilePairs {\n    identityId\n    __typename\n  }\n  distance {\n    km\n    mi\n    __typename\n  }\n  location {\n    ...ProfileLocationFragment\n    __typename\n  }\n  photos {\n    ...PhotoCarouselPictureFragment\n    __typename\n  }\n  __typename\n}\n\nfragment ProfileLocationFragment on ProfileLocation {\n  ... on DeviceLocation {\n    device {\n      latitude\n      longitude\n      geocode {\n        city\n        country\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ... on VirtualLocation {\n    core\n    __typename\n  }\n  ... on TeleportLocation {\n    current: device {\n      city\n      country\n      __typename\n    }\n    teleport {\n      latitude\n      longitude\n      geocode {\n        city\n        country\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PhotoCarouselPictureFragment on Picture {\n  id\n  pictureIsPrivate\n  pictureIsSafe\n  pictureStatus\n  pictureType\n  pictureUrl\n  publicId\n  __typename\n}",
        }
        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return None

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to get likes - Unknown error[{res.status_code}]")
            return None

        return WhoLikesMeResponse.parse_response(res.json())

    async def get_pings(
        self,
        sort_by: Literal["LAST_INTERACTION", "LAST_ONLINE", "DISTANCE"] = "LAST_INTERACTION",
        limit: int = 10,
        next_page_cursor: str | None = None,
    ) -> WhoPingsMeResponse | None:
        """
        Get users who pinged you
        :param sort_by: Sort users by last interaction, last online or distance (closest to you)
        :param limit: Number of users to get
        :param next_page_cursor: Cursor to get the next page of users
        """
        payload = {
            "operationName": "WhoPingsMe",
            "variables": {"sortBy": sort_by, "limit": limit}
            if next_page_cursor is None
            else {"sortBy": sort_by, "limit": limit, "cursor": next_page_cursor},
            "query": "query WhoPingsMe($limit: Int, $cursor: String, $sortBy: SortBy!) {\n  interactions: whoPingsMe(\n    input: {sortBy: $sortBy}\n    limit: $limit\n    cursor: $cursor\n  ) {\n    nodes {\n      ...LikesProfileFragment\n      __typename\n    }\n    pageInfo {\n      total\n      hasNextPage\n      nextPageCursor\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment LikesProfileFragment on Profile {\n  id\n  age\n  gender\n  status\n  lastSeen\n  isUplift\n  sexuality\n  isMajestic\n  isVerified\n  dateOfBirth\n  streamUserId\n  imaginaryName\n  interactionStatus {\n    message\n    mine\n    theirs\n    __typename\n  }\n  profilePairs {\n    identityId\n    __typename\n  }\n  distance {\n    km\n    mi\n    __typename\n  }\n  location {\n    ...ProfileLocationFragment\n    __typename\n  }\n  photos {\n    ...PhotoCarouselPictureFragment\n    __typename\n  }\n  __typename\n}\n\nfragment ProfileLocationFragment on ProfileLocation {\n  ... on DeviceLocation {\n    device {\n      latitude\n      longitude\n      geocode {\n        city\n        country\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ... on VirtualLocation {\n    core\n    __typename\n  }\n  ... on TeleportLocation {\n    current: device {\n      city\n      country\n      __typename\n    }\n    teleport {\n      latitude\n      longitude\n      geocode {\n        city\n        country\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PhotoCarouselPictureFragment on Picture {\n  id\n  pictureIsPrivate\n  pictureIsSafe\n  pictureStatus\n  pictureType\n  pictureUrl\n  publicId\n  __typename\n}",
        }
        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return None

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to get pings - Unknown error[{res.status_code}]")
            return None

        return WhoPingsMeResponse.parse_response(res.json())

    async def send_like(self, profile_id: str) -> bool:
        # payload = {
        #     "operationName": "ProfileLike",
        #     "variables": {"targetProfileId": profile_id},
        #     "query": "mutation ProfileLike($targetProfileId: String!) {\n  profileLike(input: {targetProfileId: $targetProfileId}) {\n    status\n    chat {\n      ...ChatListItemChatFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ChatListItemChatFragment on Chat {\n  ...ChatFragment\n  __typename\n}\n\nfragment ChatFragment on Chat {\n  id\n  name\n  type\n  streamChatId\n  status\n  ...ChatSettingsChatFragment\n  members {\n    ...ChatMemberFragment\n    __typename\n  }\n  disconnectedMembers {\n    ...ChatMemberFragment\n    __typename\n  }\n  __typename\n}\n\nfragment ChatSettingsChatFragment on Chat {\n  id\n  __typename\n}\n\nfragment ChatMemberFragment on Profile {\n  id\n  status\n  analyticsId\n  imaginaryName\n  streamUserId\n  age\n  dateOfBirth\n  sexuality\n  isIncognito\n  ...ProfileInteractionStatusFragment\n  gender\n  photos {\n    ...GetPictureUrlFragment\n    pictureType\n    __typename\n  }\n  ...AnalyticsProfileFragment\n  __typename\n}\n\nfragment ProfileInteractionStatusFragment on Profile {\n  interactionStatus {\n    message\n    mine\n    theirs\n    __typename\n  }\n  __typename\n}\n\nfragment GetPictureUrlFragment on Picture {\n  id\n  publicId\n  pictureIsSafe\n  pictureIsPrivate\n  pictureUrl\n  __typename\n}\n\nfragment AnalyticsProfileFragment on Profile {\n  id\n  isUplift\n  lastSeen\n  age\n  gender\n  sexuality\n  distance {\n    km\n    mi\n    __typename\n  }\n  profilePairs {\n    identityId\n    __typename\n  }\n  __typename\n}",
        # }
        payload = {
            "operationName": "ProfileLike",
            "variables": {"targetProfileId": profile_id},
            "query": "mutation ProfileLike($targetProfileId: String!) {\n  profileLike(input: {targetProfileId: $targetProfileId}) {\n    status\n    chat {\n      ...ChatListItemChatFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ChatListItemChatFragment on Chat {\n  ...ChatFragment\n  __typename\n}\n\nfragment ChatFragment on Chat {\n  id\n  name\n  type\n  streamChatId\n  status\n  members {\n    ...ChatMemberFragment\n    __typename\n  }\n  disconnectedMembers {\n    ...ChatMemberFragment\n    __typename\n  }\n  __typename\n}\n\nfragment ChatMemberFragment on Profile {\n  id\n  status\n  analyticsId\n  imaginaryName\n  streamUserId\n  age\n  dateOfBirth\n  sexuality\n  isIncognito\n  ...ProfileInteractionStatusFragment\n  gender\n  photos {\n    ...GetPictureUrlFragment\n    pictureType\n    __typename\n  }\n  ...AnalyticsProfileFragment\n  __typename\n}\n\nfragment ProfileInteractionStatusFragment on Profile {\n  interactionStatus {\n    message\n    mine\n    theirs\n    __typename\n  }\n  __typename\n}\n\nfragment GetPictureUrlFragment on Picture {\n  id\n  publicId\n  pictureIsSafe\n  pictureIsPrivate\n  pictureUrl\n  __typename\n}\n\nfragment AnalyticsProfileFragment on Profile {\n  id\n  isUplift\n  lastSeen\n  age\n  gender\n  sexuality\n  verificationStatus\n  distance {\n    km\n    mi\n    __typename\n  }\n  profilePairs {\n    identityId\n    __typename\n  }\n  __typename\n}",
        }

        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return False

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json() or "you have no likes left" in res.text:
            self._logger.error(f"Failed to send likes - Unknown error[{res.status_code}]")
            return False

        return True

    async def send_dislike(self, profile_id: str) -> bool:
        payload = {
            "operationName": "ProfileDislike",
            "variables": {"targetProfileId": profile_id},
            "query": "mutation ProfileDislike($targetProfileId: String!) {\n  profileDislike(input: {targetProfileId: $targetProfileId})\n}",
        }
        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return False

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to send dislikes - Unknown error[{res.status_code}]")
            return False

        return True

    async def send_ping(self, profile_id: str, message: str) -> bool:
        payload = {
            "operationName": "ProfilePing",
            "variables": {
                "targetProfileId": profile_id,
                "message": message,
                "overrideInappropriate": False,
            },
            "query": "mutation ProfilePing($targetProfileId: String!, $message: String, $overrideInappropriate: Boolean) {\n  profilePing(\n    input: {targetProfileId: $targetProfileId, message: $message, overrideInappropriate: $overrideInappropriate}\n  ) {\n    status\n    chat {\n      ...ChatListItemChatFragment\n      __typename\n    }\n    account {\n      id\n      availablePings\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ChatListItemChatFragment on Chat {\n  ...ChatFragment\n  __typename\n}\n\nfragment ChatFragment on Chat {\n  id\n  name\n  type\n  streamChatId\n  status\n  members {\n    ...ChatMemberFragment\n    __typename\n  }\n  disconnectedMembers {\n    ...ChatMemberFragment\n    __typename\n  }\n  __typename\n}\n\nfragment ChatMemberFragment on Profile {\n  id\n  status\n  analyticsId\n  imaginaryName\n  streamUserId\n  age\n  dateOfBirth\n  sexuality\n  isIncognito\n  ...ProfileInteractionStatusFragment\n  gender\n  photos {\n    ...GetPictureUrlFragment\n    pictureType\n    __typename\n  }\n  ...AnalyticsProfileFragment\n  __typename\n}\n\nfragment ProfileInteractionStatusFragment on Profile {\n  interactionStatus {\n    message\n    mine\n    theirs\n    __typename\n  }\n  __typename\n}\n\nfragment GetPictureUrlFragment on Picture {\n  id\n  publicId\n  pictureIsSafe\n  pictureIsPrivate\n  pictureUrl\n  __typename\n}\n\nfragment AnalyticsProfileFragment on Profile {\n  id\n  isUplift\n  lastSeen\n  age\n  gender\n  sexuality\n  verificationStatus\n  distance {\n    km\n    mi\n    __typename\n  }\n  profilePairs {\n    identityId\n    __typename\n  }\n  __typename\n}",
        }
        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return False

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to send ping - Unknown error[{res.status_code}]")
            return False

        return True

    async def accept_ping(self, profile_id: str) -> bool:
        payload = {
            "operationName": "ProfileAcceptPing",
            "variables": {"targetProfileId": profile_id},
            "query": "mutation ProfileAcceptPing($targetProfileId: String!) {\n  profileAcceptPing(input: {targetProfileId: $targetProfileId}) {\n    status\n    chat {\n      ...ChatListItemChatFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ChatListItemChatFragment on Chat {\n  ...ChatFragment\n  __typename\n}\n\nfragment ChatFragment on Chat {\n  id\n  name\n  type\n  streamChatId\n  status\n  members {\n    ...ChatMemberFragment\n    __typename\n  }\n  disconnectedMembers {\n    ...ChatMemberFragment\n    __typename\n  }\n  __typename\n}\n\nfragment ChatMemberFragment on Profile {\n  id\n  status\n  analyticsId\n  imaginaryName\n  streamUserId\n  age\n  dateOfBirth\n  sexuality\n  isIncognito\n  ...ProfileInteractionStatusFragment\n  gender\n  photos {\n    ...GetPictureUrlFragment\n    pictureType\n    __typename\n  }\n  ...AnalyticsProfileFragment\n  __typename\n}\n\nfragment ProfileInteractionStatusFragment on Profile {\n  interactionStatus {\n    message\n    mine\n    theirs\n    __typename\n  }\n  __typename\n}\n\nfragment GetPictureUrlFragment on Picture {\n  id\n  publicId\n  pictureIsSafe\n  pictureIsPrivate\n  pictureUrl\n  __typename\n}\n\nfragment AnalyticsProfileFragment on Profile {\n  id\n  isUplift\n  lastSeen\n  age\n  gender\n  sexuality\n  distance {\n    km\n    mi\n    __typename\n  }\n  profilePairs {\n    identityId\n    __typename\n  }\n  __typename\n}",
        }
        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return False

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to accept ping - Unknown error[{res.status_code}]")
            return False

        return True

    async def reject_ping(self, profile_id: str) -> bool:
        payload = {
            "operationName": "ProfileRejectPing",
            "variables": {"targetProfileId": profile_id},
            "query": "mutation ProfileRejectPing($targetProfileId: String!) {\n  profileRejectPing(input: {targetProfileId: $targetProfileId}) {\n    id\n    __typename\n  }\n}",
        }

        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return False

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to reject ping - Unknown error[{res.status_code}]")
            return False

        return True

    async def block_user(self, profile_id: str) -> bool:
        payload = {
            "operationName": "ProfileBlock",
            "variables": {
                "input": {
                    "blockCategory": "NOT_INTERESTED",
                    "blockDetail": "",
                    "targetProfileId": profile_id,
                }
            },
            "query": "mutation ProfileBlock($input: ProfileBlockInteractionInput!) {\n  profileBlock(input: $input)\n}",
        }

        res = await self._http_manager._request(
            "POST", self._http_manager._BASE_API_URL, self._http_manager._default_headers, json=payload
        )
        if res is None:
            return False

        self._logger.debug(res.text)
        self._logger.debug(res.status_code)
        if res.status_code != 200 or "errors" in res.json():
            self._logger.error(f"Failed to block user - Unknown error[{res.status_code}]")
            return False

        return True


if __name__ == "__main__":
    import asyncio
    import logging

    logging.basicConfig(level=logging.DEBUG)

    http_manager = HTTPManager()
    http_manager.access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZGRjYTc2YzEyMzMyNmI5ZTJlODJkOGFjNDg0MWU1MzMyMmI3NmEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZjItcHJvZC01MzQ3NSIsImF1ZCI6ImYyLXByb2QtNTM0NzUiLCJhdXRoX3RpbWUiOjE3NDI4MzkzNTAsInVzZXJfaWQiOiJpVEh1SEwwbkVmVHFEYlBCZXRIdk1Sd0U0aGoyIiwic3ViIjoiaVRIdUhMMG5FZlRxRGJQQmV0SHZNUndFNGhqMiIsImlhdCI6MTc0MzQzNzU5MywiZXhwIjoxNzQzNDQxMTkzLCJlbWFpbCI6ImouamVyenlqdXJrb3dza2lAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiai5qZXJ6eWp1cmtvd3NraUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.bp-L3F5eILy2vS0F1RFnl8bKSwnVxAOuLigJH0Rfv7AVwoNi8TcAy8krS0ITFcv0EFTH7bhl07FRm2xA3G05jcjNd06QBVnQzNk1tIqnDcIZcFX697p8bEAIDLZPnAX7LgoPlT9HjqAGi2T8zp3PCakjmJtbJQLOSFv_m0R4IXMYHMGhGL0-gszUcLbG_R1OLxt05R3tYSsRO72GGJPe22iFyrphk3JHHvT6SdzERtbhi3BhCAoyhOec92tDMmXH5dayo7MUdqyKb-opjwYtD-tOb6H-cgajxar3lVBLFX1O0M7DsqWQJsVvffxK0HAxgudPymu1KQjGChlliwj3zQ"
    http_manager.profile_id = "profile#bbaf281f-f77b-41a1-932c-1e150df54692"

    profile_manager = DiscoveryManager(http_manager)

    async def main() -> None:
        likes = await profile_manager.get_likes()
        print(len(likes.interactions.nodes))

    asyncio.run(main())
