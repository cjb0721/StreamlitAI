import os
import base64
from settings import (
    OPENAI_API_TYPE,
    OPENAI_API_BASE,
    OPENAI_API_KEY,
    OPENAI_API_VERSION
)
import main

os.environ.update({
    "OPENAI_API_TYPE": OPENAI_API_TYPE,
    "OPENAI_API_BASE": OPENAI_API_BASE,
    "OPENAI_API_KEY": base64.b64decode(OPENAI_API_KEY).decode("utf-8"),
    "OPENAI_API_VERSION": OPENAI_API_VERSION,
})

__all__ = ["main"]
