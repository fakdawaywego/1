import requests
from typing import Dict, Any, Optional
import time
from config import YANDEX_GEOCODER_API_URL, YANDEX_GEOCODER_API_KEY, logger

# Кэш для хранения результатов геокодирования
geocoding_cache = {}
# Время жизни кэша в секундах (1 час)
CACHE_EXPIRATION = 3600

def get_coordinates(city_name: str) -> Optional[Dict[str, Any]]:
    """
    Получает координаты по названию города с использованием Яндекс.Геокодера
    
    Args:
        city_name: Название города
        
    Returns:
        Словарь с координатами и информацией о местоположении или None в случае ошибки
    """

    # Проверяем кэш
    if city_name.lower() in geocoding_cache:
        cache_data, timestamp = geocoding_cache[city_name.lower()]
        # Если кэш не устарел, возвращаем данные из кэша
        if time.time() - timestamp < CACHE_EXPIRATION:
            logger.info(f"Использованы кэшированные данные для города: {city_name}")
            return cache_data
    
    logger.info(f"Запрос координат для города: {city_name}")

    params = {
        "apikey": YANDEX_GEOCODER_API_KEY,
        "format": "json",
        "geocode": city_name,
        "results": 1
    }
    
    try:
        response = requests.get(YANDEX_GEOCODER_API_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Проверяем, есть ли результаты
        feature_members = data.get("response", {}).get("GeoObjectCollection", {}).get("featureMember", [])
        if not feature_members:
            return None
            
        geo_object = feature_members[0].get("GeoObject", {})
        
        # Получаем координаты (в формате "долгота широта")
        point_str = geo_object.get("Point", {}).get("pos", "")
        if not point_str:
            return None
            
        # Разбиваем строку координат и меняем порядок (нужно "широта долгота")
        longitude, latitude = map(float, point_str.split())
        
        # Получаем название местоположения
        name = geo_object.get("name", "")
        description = geo_object.get("description", "")
        
        # Формируем результат
        result = {
            "latitude": latitude,
            "longitude": longitude,
            "display_name": f"{name}, {description}" if description else name
        }
        
        # Сохраняем в кэш
        geocoding_cache[city_name.lower()] = (result, time.time())
        
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к Яндекс.Геокодеру: {e}")
        return None