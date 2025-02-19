from typing import Any

from feeld.models.base import BaseResponse


class SignInResponse(BaseResponse):
    kind: str | None = None
    id_token: str | None = None
    email: str | None = None
    refresh_token: str | None = None
    expires_in: str | None = None
    local_id: str | None = None
    is_new_user: bool | None = None

    @classmethod
    def parse_response(cls, data: dict[str, Any]) -> "SignInResponse":
        return cls(**data)


if __name__ == "__main__":
    data = {
        "kind": "identitytoolkit#EmailLinkSigninResponse",
        "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNjNWU0MTg0M2M1ZDUyZTY4ZWY1M2UyYmVjOTgxNDNkYTE0NDkwNWUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZjItcHJvZC01MzQ3NSIsImF1ZCI6ImYyLXByb2QtNTM0NzUiLCJhdXRoX3RpbWUiOjE3MjU1MzA3MzUsInVzZXJfaWQiOiJpYUpYMzM1Tmp1T2ZXem1BV3dqbkFiY2FKdkoyIiwic3ViIjoiaWFKWDMzNU5qdU9mV3ptQVd3am5BYmNhSnZKMiIsImlhdCI6MTcyNTUzMDczNSwiZXhwIjoxNzI1NTM0MzM1LCJlbWFpbCI6InNpbW1vbi5idWlzbmVzc0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJzaW1tb24uYnVpc25lc3NAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.Hw2ah1oNkLhxo4Wx2ezg4H5U1y2zNWpLkITFO1y1sR-zGbMT1Prw3e6AFDZx1pzqYeO-KD8fx6JJdA7eVmeGqHoZF5lV7XuhBRur6waZkuGh9EMpPQH8Mvpb-nPYbb2XBaKEX-7bZqrVLDBWkGVnI5v7QFjY09Mcuw-W0kuiRPoclWFqRZMs1nx_LctFH2Wi89Ojkocb7sR0MnZJTT9kfOoXqZstAbHBhFgqmOInqgw5LEytHjOeozHxHQHAS73jRe8lZhfYlfUD1CJsWsDfLgCYYqMAkWBVtFlpq8GeS3FCq-O2yYEIgToRI9yJEoQsSN1BAvYcUYXqgumCucPEUw",
        "email": "simmon.buisness@gmail.com",
        "refreshToken": "AMf-vBwcqgRSCbhM3P9v478TrZhjw3vbWpynIy9Krf5dKyHbuNS7vB48QlpfQBMbuYQycrTzn4FC10rFmsa15cBz9q8k6sZKSvESIfKkm9eiAkVJofu8CveAAjcbysHDvbIB-6ROwn_as5n1rJBgP-ZOcdlioM4SPgQHpE92kDPzOsoXFGBWaJ8BNJBg_KQf1C0QD3WzspX_VYRTjeIphNVCX4gP9S4K_w",
        "expiresIn": "3600",
        "localId": "iaJX335NjuOfWzmAWwjnAbcaJvJ2",
        "isNewUser": False,
    }

    response = SignInResponse.parse_response(data)
    print(response)
