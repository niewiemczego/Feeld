import logging
import random
from typing import Any, Literal

import noble_tls
from noble_tls import Client
from noble_tls.response import Response

from feeld.models import AuthProviderResponse, SignInResponse
from feeld.networking.proxy_manager import ProxyManager


class HTTPManager:
    _BASE_API_URL = "https://core.api.fldcore.com/graphql"
    _BASE_CHAT_URL = "https://chat.stream-io-api.com"
    _logger = logging.getLogger(__name__)

    def __init__(self, proxy_manager: ProxyManager | None = None, refresh_token: str | None = None) -> None:
        self._proxy_manager = proxy_manager
        self._session = noble_tls.Session(client=Client.CHROME_131, random_tls_extension_order=True)
        self._access_token: str | None = None
        self._refresh_token: str | None = refresh_token
        self._profile_id: str | None = None
        self._stream_token: str | None = None
        self._stream_id: str | None = None
        self._default_headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "content-type": "application/json",
            "x-profile-id": self._profile_id,
            "x-device-os": "ios",
            "user-agent": "feeld-mobile",
            "x-app-version": "7.25.0",
        }
        self._default_headers_chat = {
            "accept-language": "en-GB,en;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "content-type": "application/json",
            "accept": "application/json, text/plain, */*",
            "stream-auth-type": "jwt",
            "x-stream-client": "stream-chat-react-native-ios-5.32.1",
            "user-agent": "Feeld/1490 CFNetwork/1390 Darwin/22.0.0",
        }

    @property
    def access_token(self) -> str | None:
        return self._access_token

    @access_token.setter
    def access_token(self, value: str) -> None:
        token = value.removeprefix("Bearer ")
        self._access_token = token
        self._default_headers["authorization"] = f"Bearer {token}"

    @property
    def profile_id(self) -> str | None:
        return self._profile_id

    @profile_id.setter
    def profile_id(self, value: str) -> None:
        self._profile_id = value
        self._default_headers["x-profile-id"] = value

    @property
    def stream_token(self) -> str | None:
        return self._stream_token

    @stream_token.setter
    def stream_token(self, value: str) -> None:
        self._stream_token = value
        self._default_headers_chat["authorization"] = value

    async def refresh_access_token(self, refresh_token: str) -> SignInResponse | None:
        payload = {
            "grantType": "refresh_token",
            "refreshToken": refresh_token,
        }

        response = await self._request(
            "POST",
            "https://securetoken.googleapis.com/v1/token?key=AIzaSyD9o9mzulN50-hqOwF6ww9pxUNUxwVOCXA",
            headers={
                "content-type": "application/json",
                "accept": "*/*",
                "x-client-version": "iOS/FirebaseSDK/10.20.0/FirebaseCore-iOS",
                "x-ios-bundle-identifier": "com.3nder.threender",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en",
                "user-agent": "FirebaseAuth.iOS/10.20.0 com.3nder.threender/7.18.0 iPhone/17.5.1 hw/iPhone14_5",
            },
            json=payload,
        )

        if response is None:
            self._logger.error("No response received during token refresh.")
            return None

        if response.status_code != 200:
            self._logger.error("Failed to refresh token: status %s", response.status_code)
            return None

        res_json = response.json()
        if "errors" in res_json:
            self._logger.error(f"Errors in token refresh response: {res_json}")
            return None

        return SignInResponse.parse_response(res_json)

    def _set_profile_data(self, profile_data: AuthProviderResponse) -> bool:
        """
        Sets profile data from an authentication provider response such as `profile_id`, `stream_token`, and `stream_id`.
        """
        if profile_data.account is None:
            self._logger.error("Failed to get account data")
            return False

        try:
            self.profile_id = profile_data.account.profiles[0].id
            self.stream_token = profile_data.account.profiles[0].stream_token
            self.stream_id = profile_data.account.profiles[0].stream_user_id
            return True
        except (KeyError, IndexError):
            return False

    async def _request(
        self, method: Literal["GET", "POST", "PUT", "DELETE"], url: str, headers: dict[str, Any], **kwargs
    ) -> Response | None:
        try:
            response = await self._session.execute_request(method, url, headers=headers, timeout_seconds=45, **kwargs)

            if self._is_token_expired(response):
                self._logger.info("Access token expired, attempting token refresh.")
                self._logger.debug(f"Response: {response.text}")
                if self._refresh_token is None:
                    self._logger.error("No refresh token set.")
                    return None

                new_token = await self.refresh_access_token(self._refresh_token)
                if new_token is None:
                    self._logger.error("Token refresh failed.")
                    return None

                self.access_token = new_token.id_token
                headers.update({"authorization": f"Bearer {self.access_token}"})
                response = await self._session.execute_request(
                    method, url, headers=headers, timeout_seconds=45, **kwargs
                )

            return response
        except Exception as e:
            self._logger.error(f"Failed to make request: {e}")
        return None

    def _is_token_expired(self, response: Response) -> bool:
        """
        Determines if the response JSON contains a token expiration error.
        """
        try:
            data = response.json()
            return (
                data.get("errors", [{}])[0].get("extensions", {}).get("originalError", {}).get("statusCode") == 401
                or "unauthorized" in response.text.lower()
                or "token_missing" in response.text.lower()
            )
        except Exception as e:
            self._logger.error(f"Error parsing response JSON: {e}")
        return False
