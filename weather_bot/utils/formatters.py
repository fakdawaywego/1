from typing import Dict, Any
from datetime import datetime

def get_weather_description(weather_code: int) -> str:
    """
    Преобразует код погоды WMO в текстовое описание на русском языке
    
    Args:
        weather_code: Код погоды WMO
        
    Returns:
        Текстовое описание погоды
    """
    weather_descriptions = {
        0: "Ясно",
        1: "Преимущественно ясно",
        2: "Переменная облачность",
        3: "Пасмурно",
        45: "Туман",
        48: "Туман с инеем",
        51: "Легкая морось",
        53: "Умеренная морось",
        55: "Сильная морось",
        61: "Небольшой дождь",
        63: "Умеренный дождь",
        65: "Сильный дождь",
        71: "Небольшой снег",
        73: "Умеренный снег",
        75: "Сильный снег",
        80: "Небольшой ливень",
        81: "Умеренный ливень",
        82: "Сильный ливень",
        95: "Гроза",
        96: "Гроза с небольшим градом",
        99: "Гроза с сильным градом"
    }
    
    return weather_descriptions.get(weather_code, "Неизвестные погодные условия")

def get_weather_emoji(weather_code: int) -> str:
    """
    Возвращает эмодзи, соответствующее коду погоды
    
    Args:
        weather_code: Код погоды WMO
        
    Returns:
        Эмодзи для отображения погоды
    """
    weather_emoji = {
        0: "☀️",  # Ясно
        1: "🌤️",  # Преимущественно ясно
        2: "⛅",  # Переменная облачность
        3: "☁️",  # Пасмурно
        45: "🌫️",  # Туман
        48: "🌫️❄️",  # Туман с инеем
        51: "🌦️",  # Легкая морось
        53: "🌦️",  # Умеренная морось
        55: "🌧️",  # Сильная морось
        61: "🌧️",  # Небольшой дождь
        63: "🌧️",  # Умеренный дождь
        65: "🌧️",  # Сильный дождь
        71: "🌨️",  # Небольшой снег
        73: "🌨️",  # Умеренный снег
        75: "❄️",  # Сильный снег
        80: "🌦️",  # Небольшой ливень
        81: "🌧️",  # Умеренный ливень
        82: "⛈️",  # Сильный ливень
        95: "⛈️",  # Гроза
        96: "⛈️🧊",  # Гроза с небольшим градом
        99: "⛈️🧊"   # Гроза с сильным градом
    }
    
    return weather_emoji.get(weather_code, "❓")

def format_current_weather(weather_data: Dict[str, Any], location_name: str) -> str:
    """
    Форматирует данные о текущей погоде в читаемый текст
    
    Args:
        weather_data: Данные о погоде от API Open-Meteo
        location_name: Название местоположения
        
    Returns:
        Отформатированный текст с информацией о погоде
    """
    current = weather_data.get("current", {})
    
    if not current:
        return "Не удалось получить данные о текущей погоде."
    
    temperature = current.get("temperature_2m")
    humidity = current.get("relative_humidity_2m")
    wind_speed = current.get("wind_speed_10m")
    weather_code = current.get("weather_code")
    
    weather_desc = get_weather_description(weather_code)
    emoji = get_weather_emoji(weather_code)
    
    # Получаем текущее время в часовом поясе местоположения
    current_time = current.get("time")
    if current_time:
        time_str = f"Данные на {current_time}"
    else:
        time_str = "Текущие данные"
    
    result = f"*Погода в {location_name}* {emoji}\n\n"
    result += f"🌡️ Температура: *{temperature}°C*\n"
    result += f"💧 Влажность: {humidity}%\n"
    result += f"💨 Скорость ветра: {wind_speed} км/ч\n"
    result += f"🔍 Условия: {weather_desc}\n\n"
    result += f"_{time_str}_"
    
    return result

def format_forecast(forecast_data: Dict[str, Any], location_name: str) -> str:
    """
    Форматирует данные о прогнозе погоды в читаемый текст
    
    Args:
        forecast_data: Данные о прогнозе от API Open-Meteo
        location_name: Название местоположения
        
    Returns:
        Отформатированный текст с информацией о прогнозе
    """
    daily = forecast_data.get("daily", {})
    
    if not daily or not daily.get("time"):
        return "Не удалось получить данные о прогнозе погоды."
    
    result = f"*Прогноз погоды для {location_name}*\n\n"
    
    # Названия дней недели на русском
    weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    
    for i in range(len(daily["time"])):
        date_str = daily["time"][i]
        max_temp = daily["temperature_2m_max"][i]
        min_temp = daily["temperature_2m_min"][i]
        precip = daily["precipitation_sum"][i]
        weather_code = daily["weather_code"][i]
        
        # Получаем день недели
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        weekday = weekdays[date_obj.weekday()]
        
        # Форматируем дату
        formatted_date = date_obj.strftime("%d.%m.%Y")
        
        emoji = get_weather_emoji(weather_code)
        weather_desc = get_weather_description(weather_code)
        
        result += f"*{weekday}, {formatted_date}* {emoji}\n"
        result += f"🌡️ Температура: от *{min_temp}°C* до *{max_temp}°C*\n"
        result += f"💧 Осадки: {precip} мм\n"
        result += f"🔍 Условия: {weather_desc}\n\n"
    
    return result