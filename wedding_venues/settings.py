# Scrapy settings for wedding_venues project

BOT_NAME = "wedding_venues"

SPIDER_MODULES = ["wedding_venues.spiders"]
NEWSPIDER_MODULE = "wedding_venues.spiders"

# User-Agent to mimic a real browser
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Ignore robots.txt to avoid restrictions
ROBOTSTXT_OBEY = False

# Increase concurrency to speed up scraping
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8

# Set a reasonable download delay to prevent getting blocked
DOWNLOAD_DELAY = 0  # Reduce if needed

# Enable AutoThrottle to adjust request rates dynamically
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 3.0
AUTOTHROTTLE_DEBUG = False

# Enable Splash for JavaScript-rendered pages
SPLASH_URL = 'http://localhost:8050'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,  # Added retry in case of failures
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Avoid duplicate filtering issues
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Enable cache to avoid reloading pages unnecessarily
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600  # Cache pages for 1 hour
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 403, 404]

# Feed export encoding
FEED_EXPORT_ENCODING = "utf-8"

# Improve logging to debug pagination issues
LOG_LEVEL = 'DEBUG'
LOG_ENABLED = True

# Allow retries in case of temporary bans
RETRY_ENABLED = True
RETRY_TIMES = 3  # Retry up to 3 times on failure
RETRY_HTTP_CODES = [500, 502, 503, 504, 408]
