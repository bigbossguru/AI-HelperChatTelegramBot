import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - [%(filename)s > %(funcName)s()] - %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler("bot_logger.log", mode="w"),
        # logging.StreamHandler(sys.stdout),
    ],
)

# logger = logging.getLogger(__name__)
