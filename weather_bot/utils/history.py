import json
import os
from datetime import datetime
from typing import Dict, List, Any
from config import logger

# Путь к файлу с историей запросов
HISTORY_FILE = "data/history.json"

def ensure_data_dir():
    """Создает директорию для данных, если она не существует"""
    os.makedirs("data", exist_ok=True)

def save_request_to_history(user_id: int, user_name: str, city: str, request_type: str) -> None:
    """
    Сохраняет запрос пользователя в историю
    
    Args:
        user_id: ID пользователя
        user_name: Имя пользователя
        city: Название города
        request_type: Тип запроса (weather/forecast)
    """
    ensure_data_dir()
    
    # Текущее время
    timestamp = datetime.now().isoformat()
    
    # Данные для сохранения
    request_data = {
        "user_id": user_id,
        "user_name": user_name,
        "city": city,
        "request_type": request_type,
        "timestamp": timestamp
    }
    
    try:
        # Загружаем существующую историю
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                history = json.load(file)
        
        # Добавляем новый запрос
        history.append(request_data)
        
        # Сохраняем обновленную историю
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=2)
        
        logger.info(f"Запрос сохранен в историю: {user_id} - {city} ({request_type})")
    except Exception as e:
        logger.error(f"Ошибка при сохранении запроса в историю: {e}")

def get_user_history(user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Получает историю запросов пользователя
    
    Args:
        user_id: ID пользователя
        limit: Максимальное количество записей
        
    Returns:
        Список последних запросов пользователя
    """
    try:
        if not os.path.exists(HISTORY_FILE):
            return []
        
        # Загружаем историю
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)
        
        # Фильтруем записи по user_id и сортируем по времени (от новых к старым)
        user_history = [
            item for item in history if item["user_id"] == user_id
        ]
        user_history.sort(key=lambda x: x["timestamp"], reverse=True)
        
        # Возвращаем ограниченное количество записей
        return user_history[:limit]
    except Exception as e:
        logger.error(f"Ошибка при получении истории пользователя: {e}")
        return []