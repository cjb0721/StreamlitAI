import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_PATH, "data")
HISTORY_DIR = os.path.join(BASE_PATH, "history")

OPENAI_API_TYPE = "azure"
OPENAI_API_BASE = "https://bcrdcaitest.openai.azure.com/"
OPENAI_API_KEY = "OTI4MTE4ZmNmMTYwNDZiMGExMjQ5Njk3NTY1OTRhZTA="
OPENAI_API_VERSION = "2023-05-15"

# Test login account
# Generate hash password to replace credentials password:
#   hashed_passwords = stauth.Hasher(['123', '456']).generate()
TEST_ACCOUNT = {
    "usernames": {
        "123@qq.com": {
            "email": "123@qq.com",
            "name": "Tom",
            "password": '$2b$12$45ytHf5389ytssBoCZFQnuvsmkvwHpC2/.DXVwtH5mr0xdnC2h0Vm'
        },
        "456@qq.com": {
            "email": "456@qq.com",
            "name": "Jerry456",
            "password": '$2b$12$JamShiG7HepBTdPAo1zZHOpnzFVZyMNpeA5Onbz0KrywAWr5wK1SK'
        }
    }
}

# The list of emails of unregistered users authorized to register
PREAUTHORIZED = ["abc@qq.com", "def@qq.com"]

HIDE_DEFAULT_FORMAT = """
    <style>
        footer {visibility: hidden;}
    </style>
"""
