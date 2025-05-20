from telegram import Update
from telegram.ext import CallbackContext
from utils.history import get_user_history
from config import logger
from datetime import datetime

def history_command(update: Update, context: CallbackContext) -> None:
    """
    Обрабатывает команду /history
    
    Args:
        update: Объект с информацией о сообщении
        context: Контекст обработчика
    """
    user = update.effective_user
    logger.info(f"Пользователь {user.id} запросил историю запросов")
    
    # Получаем историю запросов пользователя
    history = get_user_history(user.id)
    
    if not history:
        update.message.reply_text(
            "У вас пока нет истории запросов."
        )
        return
    
    # Форматируем историю
    message = "*Ваша история запросов:*\n\n"
    
    for i, item in enumerate(history, 1):
        # Преобразуем строку времени в объект datetime
        timestamp = datetime.fromisoformat(item["timestamp"])
        # Форматируем время
        formatted_time = timestamp.strftime("%d.%m.%Y %H:%M")
        
        # Определяем тип запроса
        request_type = "Погода" if item["request_type"] == "weather" else "Прогноз"
        
        message += f"{i}. {request_type} для города *{item['city']}*\n"
        message += f"   _({formatted_time})_\n"
    
    update.message.reply_text(
        message,
        parse_mode="Markdown"
    )