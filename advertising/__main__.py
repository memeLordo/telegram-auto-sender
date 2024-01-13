import advertising.start_spam as start_spam
from loguru import logger

logger.add(
    "advertising/ads_main.log",
    format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="10 MB",
    retention="2 days",
    compression="zip",
)

start_spam.main()
