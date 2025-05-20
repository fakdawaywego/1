import os
from dotenv import load_dotenv
from utils.logger import setup_logger

# Загрузка переменных окружения из файла .env
load_dotenv()

# Настройка логгера
logger = setup_logger()

# Токен Telegram бота
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TELEGRAM_TOKEN:
    logger.error("Токен Telegram бота не найден в переменных окружения")
    raise ValueError("Токен Telegram бота не найден в переменных окружения")

# Настройки для API погоды
WEATHER_API_URL = 'https://api.open-meteo.com/v1/forecast'

# Настройки для API геокодирования
GEOCODING_API_URL = 'https://nominatim.openstreetmap.org/search'
GEOCODING_USER_AGENT = 'WeatherBot/1.0'

# Настройки кэширования
CACHE_EXPIRATION = 3600  # Время жизни кэша в секундах (1 час)

# Настройки для Яндекс.Геокодера
YANDEX_GEOCODER_API_URL = 'https://geocode-maps.yandex.ru/1.x/'
YANDEX_GEOCODER_API_KEY = os.getenv('YANDEX_GEOCODER_API_KEY')

# Настройки кэширования
CACHE_EXPIRATION = 1800  # Время жизни кэша в секундах (30 минут)