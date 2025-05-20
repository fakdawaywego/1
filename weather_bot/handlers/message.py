from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext
from config import logger
from .weather import get_weather_for_city
from .forecast import get_forecast_for_city

def text_message(update: Update, context: CallbackContext) -> None:
    """
    Обрабатывает текстовые сообщения
    
    Args:
        update: Объект с информацией о сообщении
        context: Контекст обработчика
    """
    user = update.effective_user
    message_text = update.message.text
    
    logger.info(f"Пользователь {user.id} отправил сообщение: {message_text}")
    
    # Проверяем, ожидаем ли мы ввод города от пользователя
    if context.user_data.get("waiting_for_city"):
        # Если пользователь отменил операцию
        if message_text.lower() == "отмена":
            update.message.reply_text(
                "Операция отменена.",
                reply_markup=ReplyKeyboardRemove()
            )
            # Сбрасываем состояние ожидания
            context.user_data.pop("waiting_for_city", None)
            return
        
        # Определяем, какую команду выполнять
        command_type = context.user_data["waiting_for_city"]
        
        if command_type == "weather":
            # Получаем погоду для указанного города
            get_weather_for_city(update, context, message_text)
        elif command_type == "forecast":
            # Получаем прогноз для указанного города
            get_forecast_for_city(update, context, message_text)
    else:
        # Если нет активного состояния, предлагаем использовать команды
        update.message.reply_text(
            "Я понимаю только команды.\n"
            "Используйте /weather <город> для получения текущей погоды или\n"
            "/forecast <город> для получения прогноза на 5 дней.\n"
            "Отправьте /help для получения справки."
        )