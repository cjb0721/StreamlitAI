import os
import base64

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_PATH, "data")

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = "https://bcrdcaitest.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = base64.b64decode(
    "OTI4MTE4ZmNmMTYwNDZiMGExMjQ5Njk3NTY1OTRhZTA="
).decode("utf-8")
os.environ["OPENAI_API_VERSION"] = "2023-05-15"
