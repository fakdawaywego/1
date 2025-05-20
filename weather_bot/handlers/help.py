from telegram import Update
from telegram.ext import CallbackContext
from config import logger

def help_command(update: Update, context: CallbackContext) -> None:
    """
    Обрабатывает команду /help
    
    Args:
        update: Объект с информацией о сообщении
        context: Контекст обработчика
    """
    user = update.effective_user
    logger.info(f"Пользователь {user.id} запросил справку")
    
    # Формируем сообщение со справкой
    message = (
        "🔍 *Справка по командам*\n\n"
        "*Основные команды:*\n"
        "• /start - начать работу с ботом\n"
        "• /weather <город> - узнать текущую погоду\n"
        "• /forecast <город> - получить прогноз на 5 дней\n"
        "• /history - показать историю ваших запросов\n"
        "• /help - показать эту справку\n\n"
        "*Примеры использования:*\n"
        "• /weather Москва\n"
        "• /forecast Санкт-Петербург\n\n"
        "Вы также можете использовать кнопки под сообщениями для быстрого доступа к функциям."
    )
    
    # Отправляем сообщение с поддержкой Markdown
    update.message.reply_text(message, parse_mode='Markdown')