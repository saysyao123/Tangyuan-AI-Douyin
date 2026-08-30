from __future__ import annotations

import os


DOLA_CHAIN_SINGLE = "/im/chain/single"
DOLA_REFERER = os.getenv("DOLA_REFERER", "https://www.dola.com/")
DOLA_TIMEOUT_SECONDS = float(os.getenv("DOLA_TIMEOUT_SECONDS", "60"))

CANDIDATE_URL_KEYS = (
    "main_url",
    "man_url",
    "play_url",
    "download_url",
    "video_url",
    "url",
)
VIDEO_ID_KEYS = ("vid", "video_id", "videoId", "videoID", "key")
KEY_SEED_KEYS = ("key_seed", "keySeed")
FALLBACK_API_KEYS = ("fallback_api", "fallbackApi")
VIDEO_MODEL_KEYS = ("video_model", "videoModel")
VIDEO_LIST_KEYS = ("video_list", "videoList")

ORIGINAL_HINTS = ("original", "origin", "source", "master", "raw")
UNWATERMARKED_HINTS = (
    "logo_type=unwatermarked",
    "unwatermarked",
    "lr=unwatermarked",
    "video_gen_no_watermark",
    "lr=video_gen_no_watermark",
)
WATERMARKED_HINTS = (
    "lr=cici_ai",
    "logo_type=cici_ai",
    "logo_type=watermarked",
    "watermark=true",
    "watermark=1",
    "video_gen_watermark",
)
