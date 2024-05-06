import os

os.environ["DEBUG_TOOLBAR"] = "False"
os.environ["SUBTENSOR_ADDRESS"] = "local"
os.environ["SUBNET_UID"] = "1"
os.environ["WALLET_NAME"] = "default"
os.environ["WALLET_HOTKEY"] = "default"
os.environ["WALLET_PATH"] = ""

from bittensor_panel.settings import *  # noqa: E402,F403
