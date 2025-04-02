# Feeld

An unofficial asynchronous API wrapper for interacting with the Feeld dating app. Designed for managing multiple profiles, automating actions and facilitating account operations.

> **Disclaimer:**
>
> This project is an independent, community-driven effort and is not affiliated, endorsed, or sponsored by Feeld or Feeld Ltd. The purpose of this wrapper is solely to serve as a portfolio piece demonstrating my skills and abilities. It is **not intended to harm or misrepresent the company or its services.**

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.11+** (recommended)
- Virtual environment tool (e.g., `venv` or `pipenv`)

### Installation

```bash
git clone https://github.com/niewiemczego/Feeld.git
cd feeld
pip install -r requirements.txt
```

## TODO

- [X] HTTP(s) support
- [X] Proxy Manager
- [X] Rotating proxy automatically
- [ ] Creating(sign-up) accounts module (related to SeonSDK)
- [ ] Login(sign-in) possibility with email and password (related to SeonSDK)
- [ ] SeonSDK fingerprint support (used during sign-up / sign-in)
- [X] Refreshing access token automatically
- [X] Chat Manager (Enable sending pre-made videos alongside live recording)
- [X] Profile Manager
- [X] Discovery Manager(Swipes/Likes/Matches)
- [ ] Update some endpoints to always return data instead of True/False to allow user-defined handling (?)




## Usage

The script is divided into three main sections: `profile_manager`, `discovery_manager` and `chat_manager`.

### Initial Setup

Before using the managers, you need to initialize the `HTTPManager` and set up the profile data:

```python
import asyncio
import logging

from feeld import (
    ChatManager,
    DiscoveryManager,
    HTTPManager,
    ImageMessage,
    PopularLocations,
    ProfileManager,
    ProfileUpdatePayload,
    TextMessage,
    VideoMessage,
)

logging.basicConfig(level=logging.DEBUG)

REFRESH_TOKEN = "YOUR_REFRESH_TOKEN_HERE"  # Replace with your actual refresh token

http_manager = HTTPManager(refresh_token=REFRESH_TOKEN)

async def initial_profile_setup(http_manager: HTTPManager) -> bool:
    profile_manager = ProfileManager(http_manager)

    # Get profile data
    profile_data = await profile_manager.get_profile_data()
    if profile_data is None:
        return False

    # Set profile data in HTTPManager
    set_profile_data = http_manager._set_profile_data(profile_data)
    if not set_profile_data:
        return False

    # Update last seen status
    await profile_manager.update_last_seen_status()
    return True
```
__Important Note:__ `initial_profile_setup` should only be called once at the beginning of your script's execution. It fetches and sets up essential profile data. Calling it repeatedly for the same profile is unnecessary and can lead to inefficiencies. So generally speaking if you are going to use every manager then u should call this function in the main one instead of in each function for each manager as we do in the examples.


### Profile Manager

The `profile_manager` function demonstrates how to interact with the user profile:

```py
async def profile_manager() -> None:
    # Initial profile setup
    if not await initial_profile_setup(http_manager):
        return

    profile_manager = ProfileManager(http_manager)

    # Update profile data
    await profile_manager.update_profile(
        ProfileUpdatePayload(
            bio="We should get to know each other better, don't you think?",
            interests=["sports", "music", "art", "travel", "golf", "food"],
        ),
    )

    # Update profile location
    await profile_manager.update_profile_location(41.881832, -87.623177)
    # await profile_manager.update_profile_location(popular_location=PopularLocations.LOS_ANGELES.value)
```

### Chat Manager

The `chat_manager` function demonstrates how to manage chats, including sending likes, getting matches, and sending messages:

```py
async def chat_manager() -> None:
    # Initial profile setup
    if not await initial_profile_setup(http_manager):
        return

    chat_manager = ChatManager(http_manager)
    discovery_manager = DiscoveryManager(http_manager)

    connection_id = await chat_manager.get_connection_id()
    if connection_id is None:
        return

    # Force match by liking all users who liked you
    likes = await discovery_manager.get_likes()
    for like in likes.interactions.nodes:
        await discovery_manager.send_like(like.id)

    # Alternative: Swipe on users based on interaction status
    users_to_swipe_on = await discovery_manager.get_users_to_swipe_on([18, 30])
    for user in users_to_swipe_on.discovery.nodes:
        if user.interaction_status.theirs.upper() == "LIKED":
            await discovery_manager.send_like(user.id)
            continue

        if user.interaction_status.theirs.upper() == "PINGED":
            await discovery_manager.accept_ping(user.id)
            continue

        if user.interaction_status.theirs.upper() == "DISLIKED":
            await discovery_manager.send_dislike(user.id)
            continue

    # Get matches and their stream channel ID
    matches = await discovery_manager.get_matches()
    if not matches:
        return

    # for this example we are getting only data of the first user from matches, so that's why we are indexing [0]
    # but in real sceario you will for loop ofc
    user_chat_id = matches.summaries.nodes[0].id
    activate_chat = await chat_manager.activate_chat(user_chat_id)
    if activate_chat is None:
        return

    user_stream_channel_id = matches.summaries.nodes[0].stream_channel_id

    # Interact with the chat
    messages_history = await chat_manager.get_messages_history(user_stream_channel_id, connection_id)
    print(f"{messages_history=}")

    await chat_manager.send_video_message(
        user_stream_channel_id,
        connection_id,
        "test_video.mov",
        VideoMessage("Hey how r u ?", "view_once"),
    )

    await chat_manager.send_image_message(
        user_stream_channel_id,
        connection_id,
        "test_image.png",
        user_chat_id,
        ImageMessage("Heeyyy :))", "view_once", 10),
    )

    await chat_manager.send_text_message(
        user_stream_channel_id,
        connection_id,
        TextMessage("Wanna hang out?"),
    )
```

## Contact
For questions, suggestions or any feedback regarding the Feeld API Wrapper, please use one of the following methods:

- GitHub: Open an issue in the repository.
- Telegram: @niewiemczego
- Discord: niewiemczego

> **Job Opportunities:** I am actively looking for a Python developer position. If you have any relevant opportunities, please reach out to me via the contact methods above.

Your feedback is important and I'm happy to help!
