import random
import uuid
from dataclasses import dataclass
from typing import Any, Literal

ReplayModeType = Literal["replayable", "view_once"]
PlayableDurationType = Literal[5, 10, 15]
MessageType = Literal["text", "image"]


@dataclass
class ImageMessage:
    message_text: str = ""
    attachment_id: str | None = None
    replay_mode: ReplayModeType = "replayable"
    playable_duration: PlayableDurationType | None = None

    def __post_init__(self) -> None:
        if not self.message_text and not self.attachment_id:
            raise ValueError("You need to provide either 'message_text' or 'attachment_id'")

        if self.replay_mode == "replayable" and self.playable_duration is not None:
            print("Warning: playable_duration is ignored for 'replayable' mode")
            self.playable_duration = None
            return

        if self.replay_mode == "view_once":
            if self.playable_duration is None:
                print("Warning: playable_duration not set for 'view_once', defaulting to 5")
                self.playable_duration = 5
            elif self.playable_duration not in (5, 10, 15):
                raise ValueError(
                    f"Invalid playable_duration ({self.playable_duration}) for 'view_once'. Must be 5, 10 or 15"
                )

    def to_payload_dict(self) -> dict[str, Any]:
        message_type: MessageType = "text"
        attachments_payload: list[dict[str, Any]] = []

        if self.attachment_id:
            message_type = "image"
            attachment_properties = {"replay_mode": self.replay_mode}
            if self.replay_mode == "view_once" and self.playable_duration:
                attachment_properties["playableDuration"] = self.playable_duration

            attachments_payload = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "image",
                    "image_url": self.attachment_id,
                    "fallback": f"{uuid.uuid4()}.{random.choice(['jpg', 'png'])}",
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
    msg = ChatMessage("Would you fit there?", "chat-attachment#b5d9d966-c30a-494b-a9ad-568f21901719", "view_once", 5)
    print(msg.to_payload_dict())

    # {
    #     "message": {
    #         "id": "718d32ab-005e-4644-abbc-7034e36d0905",
    #         "text": "Would you fit there?",
    #         "mentioned_users": [],
    #         "custom_properties": {"type": "image", "status": "regular"},
    #         "attachments": [
    #             {
    #                 "properties": {"replay_mode": "view_once", "playableDuration": 5},
    #                 "id": "6fc33b08-30b5-4eb0-3165-951f62e55173",
    #                 "type": "image",
    #                 "image_url": "chat-attachment#b5d9d966-c30a-494b-a9ad-568f21901719",
    #                 "fallback": "IMG_0009.PNG",
    #             }
    #         ],
    #     },
    #     "skip_enrich_url": true,
    # }


{
    "message": {
        "id": "9ea26c43-a8a1-4232-8ffb-66d153a6d4a2",
        "text": "",
        "mentioned_users": [],
        "custom_properties": {"type": "video", "status": "regular"},
        "attachments": [
            {
                "properties": {"replay_mode": "view_once", "duration": 1774},
                "id": "e2d5a730-89eb-4ae8-0cd8-32a6d722463c",
                "type": "video",
                "url": "https://us-east.stream-io-cdn.com/61795/attachments/fc4fe060-4954-43dd-a11a-3f84b0998e39.E0FA17C9-BFCA-4AF6-84E8-7F0119B9E47D.mov?Expires=1744552454&Signature=gr4ihri7hDQj6kPXpxTlOLhwuYjqKnVl-ROi9CEAt6IvdE-wKOspnkBg-lAb5UwVzf6NLlBmkwZe9o0aJR4-4nMBHYDv7ATYBHIwz1V9F8P0Qb0fP68oCxCLNYETU4y6gsxg0o7sfJ2XOvhhOIuNkHLUVwzQThnNzO0IzW56Uikb0nd~-HvP7O75S3bROR-6P0kCC6Ypa3JqiksF~qcLLKEpQ~65NcOIeaQEd0UN-610PDlEB5fJd~hdtKl24tupw8PWT~VsJX8GyJDpdkJNOBTV1nBAq3bhwboVED9jRGSKPZURzioFwgOX-W2Ed7OLz089WlFXtalHplWdBX2AiQ__&Key-Pair-Id=APKAIHG36VEWPDULE23Q",
                "duration": 0,
            }
        ],
    },
    "skip_enrich_url": true,
}


# {
#     "message": {
#         "id": "70018176-f144-4b07-9cf9-bf5acc22c0e8",
#         "text": "Would you fit there?",
#         "mentioned_users": [],
#         "custom_properties": {"type": "image", "status": "regular"},
#         "attachments": [
#             {
#                 "id": "59e503e9-5a76-4233-9cb1-85b3a632a4b5",
#                 "type": "image",
#                 "image_url": "chat-attachment#b5d9d966-c30a-494b-a9ad-568f21901719",
#                 "fallback": "7818dbc0-bea6-4e66-9b91-ea0e9d850d4d.jpg",
#                 "properties": {"replay_mode": "view_once", "playableDuration": 5},
#             }
#         ],
#     },
#     "skip_enrich_url": True,
# }
