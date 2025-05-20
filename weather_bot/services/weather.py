import requests
from typing import Dict, Any, Optional
import time
from config import WEATHER_API_URL, logger

# Кэш для хранения результатов запросов погоды
weather_cache = {}
# Время жизни кэша в секундах (30 минут)
CACHE_EXPIRATION = 1800

def get_weather(latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
    """
    Получает данные о текущей погоде
    
    Args:
        latitude: Широта местоположения
        longitude: Долгота местоположения
        
    Returns:
        Словарь с данными о погоде или None в случае ошибки
    """
    # Создаем ключ для кэша
    cache_key = f"{latitude:.4f}_{longitude:.4f}_current"
    
    # Проверяем кэш
    if cache_key in weather_cache:
        cache_data, timestamp = weather_cache[cache_key]
        # Если кэш не устарел, возвращаем данные из кэша
        if time.time() - timestamp < CACHE_EXPIRATION:
            logger.info(f"Использованы кэшированные данные о погоде для координат: {latitude}, {longitude}")
            return cache_data
    
    logger.info(f"Запрос текущей погоды для координат: {latitude}, {longitude}")
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "timezone": "auto"
    }
    
    try:
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Сохраняем в кэш
        weather_cache[cache_key] = (data, time.time())
        
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к API погоды: {e}")
        return None

def get_forecast(latitude: float, longitude: float, days: int = 5) -> Optional[Dict[str, Any]]:
    """
    Получает прогноз погоды на несколько дней
    
    Args:
        latitude: Широта местоположения
        longitude: Долгота местоположения
        days: Количество дней для прогноза (по умолчанию 5)
        
    Returns:
        Словарь с данными о прогнозе или None в случае ошибки
    """
    # Создаем ключ для кэша
    cache_key = f"{latitude:.4f}_{longitude:.4f}_forecast_{days}"
    
    # Проверяем кэш
    if cache_key in weather_cache:
        cache_data, timestamp = weather_cache[cache_key]
        # Если кэш не устарел, возвращаем данные из кэша
        if time.time() - timestamp < CACHE_EXPIRATION:
            logger.info(f"Использованы кэшированные данные о прогнозе для координат: {latitude}, {longitude}")
            return cache_data
    
    logger.info(f"Запрос прогноза погоды на {days} дней для координат: {latitude}, {longitude}")
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": days
    }
    
    try:
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Сохраняем в кэш
        weather_cache[cache_key] = (data, time.time())
        
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к API прогноза погоды: {e}")
        return None