import random
import uuid
from dataclasses import dataclass
from typing import Any, Literal

ReplayModeType = Literal["replayable", "view_once"]
PlayableDurationType = Literal[5, 10, 15]
MessageType = Literal["text", "video"]


@dataclass
class VideoMessage:
    message_text: str = ""
    url: str | None = None
    replay_mode: ReplayModeType = "replayable"

    def __post_init__(self) -> None:
        if not self.message_text and not self.url:
            raise ValueError("You need to provide either 'message_text' or 'url'")

        if self.replay_mode not in ("replayable", "view_once"):
            raise ValueError(f"Invalid replay_mode: {self.replay_mode}")

    def to_payload_dict(self) -> dict[str, Any]:
        message_type: MessageType = "text"
        attachments_payload: list[dict[str, Any]] = []

        if self.url:
            message_type = "video"
            attachment_properties = {"replay_mode": self.replay_mode, "duration": "video duration in ms (int)"}

            attachments_payload = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "video",
                    "url": self.url,
                    "duration": 0,
                    "properties": attachment_properties,
                }
            ]

        payload = {
            "message": {
                "id": str(uuid.uuid4()),
                "text": self.message_text,
                "mentioned_users": [],
                "custom_properties": {
                    "type": message_type,
                    "status": "regular",
                },
                "attachments": attachments_payload,
            },
            "skip_enrich_url": True,
        }
        return payload


if __name__ == "__main__":
    msg = VideoMessage("elo elo ")
    print(msg.to_payload_dict())

# {
#     "message": {
#         "id": "9ea26c43-a8a1-4232-8ffb-66d153a6d4a2",
#         "text": "",
#         "mentioned_users": [],
#         "custom_properties": {"type": "video", "status": "regular"},
#         "attachments": [
#             {
#                 "properties": {"replay_mode": "view_once", "duration": 1774},
#                 "id": "e2d5a730-89eb-4ae8-0cd8-32a6d722463c",
#                 "type": "video",
#                 "url": "https://us-east.stream-io-cdn.com/61795/attachments/fc4fe060-4954-43dd-a11a-3f84b0998e39.E0FA17C9-BFCA-4AF6-84E8-7F0119B9E47D.mov?Expires=1744552454&Signature=gr4ihri7hDQj6kPXpxTlOLhwuYjqKnVl-ROi9CEAt6IvdE-wKOspnkBg-lAb5UwVzf6NLlBmkwZe9o0aJR4-4nMBHYDv7ATYBHIwz1V9F8P0Qb0fP68oCxCLNYETU4y6gsxg0o7sfJ2XOvhhOIuNkHLUVwzQThnNzO0IzW56Uikb0nd~-HvP7O75S3bROR-6P0kCC6Ypa3JqiksF~qcLLKEpQ~65NcOIeaQEd0UN-610PDlEB5fJd~hdtKl24tupw8PWT~VsJX8GyJDpdkJNOBTV1nBAq3bhwboVED9jRGSKPZURzioFwgOX-W2Ed7OLz089WlFXtalHplWdBX2AiQ__&Key-Pair-Id=APKAIHG36VEWPDULE23Q",
#                 "duration": 0,
#             }
#         ],
#     },
#     "skip_enrich_url": true,
# }

# {
# 	"message": {
# 		"id": "faa7bea9-cb23-484d-aec5-68688f60be91",
# 		"text": "",
# 		"mentioned_users": [],
# 		"custom_properties": {
# 			"type": "video",
# 			"status": "regular"
# 		},
# 		"attachments": [{
# 			"properties": {
# 				"replay_mode": "replayable",
# 				"duration": 1504
# 			},
# 			"id": "740545ea-b590-4e5e-2d0b-eaa7012d0a76",
# 			"type": "video",
# 			"url": "https://us-east.stream-io-cdn.com/61795/attachments/bec520dc-7d4c-48d1-8565-21468077cf89.E0997BBD-1371-45A8-92ED-398B1BE4D830.mov?Expires=1744555349&Signature=I9EWn3VlRvJqn1RCBYjMx5ecOTKxKdA-Jpgu72jXoa~VB-cLZwmURhSRg7gotgg-p2EBhu9POPccOblfWII-VBgI0Q4k-H1mwkkrV9vyNeQUW6y1mPYQApVBuM9xw20Vj10KQZ6xDuAktXF3SV9E6uqcK7AmnSieKi4zrGof8YSXMsWffbF5cd0PXUNS3sSUpYyX5hKLgpJ5ZSFukv84LJEAU-XjChEMYHJXdIvb3S2J9LB5ooFpF6fawNgreSbOVTtIpGkf~C6Gr-OHugJthdxDl0YrIrehHfkFn3Lr73LBHycwEYTbt9BV03Nhrdrg6rUeB1cH663k7VUlIvuZPw__&Key-Pair-Id=APKAIHG36VEWPDULE23Q",
# 			"duration": 0
# 		}]
# 	},
# 	"skip_enrich_url": true
# }
