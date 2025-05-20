from telegram import Update
from telegram.ext import CallbackContext
from config import logger
from .weather import get_weather_for_city
from .forecast import get_forecast_for_city

def button_callback(update: Update, context: CallbackContext) -> None:
    """
    Обрабатывает нажатия на инлайн-кнопки
    
    Args:
        update: Объект с информацией о сообщении
        context: Контекст обработчика
    """
    query = update.callback_query
    user = query.from_user
    
    # Получаем данные из callback_data
    callback_data = query.data
    logger.info(f"Пользователь {user.id} нажал кнопку: {callback_data}")
    
    # Отправляем уведомление о получении запроса
    query.answer()
    
    # Обрабатываем различные типы callback_data
    if callback_data.startswith("weather_"):
        # Запрос текущей погоды
        city = callback_data[8:]  # Получаем название города
        # Создаем фиктивное сообщение для обработчика
        update.message = query.message
        get_weather_for_city(update, context, city)
    
    elif callback_data.startswith("forecast_"):
        # Запрос прогноза
        city = callback_data[9:]  # Получаем название города
        # Создаем фиктивное сообщение для обработчика
        update.message = query.message
        get_forecast_for_city(update, context, city)
    
    elif callback_data.startswith("refresh_weather_"):
        # Обновление данных о погоде
        city = callback_data[15:]  # Получаем название города
        # Создаем фиктивное сообщение для обработчика
        update.message = query.message
        get_weather_for_city(update, context, city)
    
    elif callback_data.startswith("refresh_forecast_"):
        # Обновление прогноза
        city = callback_data[16:]  # Получаем название города
        # Создаем фиктивное сообщение для обработчика
        update.message = query.message
        get_forecast_for_city(update, context, city)