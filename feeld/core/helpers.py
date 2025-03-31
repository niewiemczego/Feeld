import math
import mimetypes
import sys

import ffmpeg


def get_file_content_type(file_path: str) -> str | None:
    mime_type, encoding = mimetypes.guess_type(file_path)
    return mime_type


def get_video_duration(video_path: str) -> int:
    try:
        probe = ffmpeg.probe(video_path)
        duration_sec = None
        if "format" in probe and "duration" in probe["format"]:
            duration_sec = float(probe["format"]["duration"])
        else:
            for stream in probe.get("streams", []):
                if "duration" in stream:
                    duration_sec = float(stream["duration"])
                    break

        if duration_sec is not None:
            duration_ms = int(math.ceil(duration_sec * 1000))
            return duration_ms
        else:
            print(f"Warning: Could not find duration info for {video_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
    return 0
