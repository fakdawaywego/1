from telegram import Update
from telegram.ext import CallbackContext
from config import logger

def start_command(update: Update, context: CallbackContext) -> None:
    """
    Обрабатывает команду /start
    
    Args:
        update: Объект с информацией о сообщении
        context: Контекст обработчика
    """
    user = update.effective_user
    logger.info(f"Пользователь {user.id} ({user.username}) запустил бота")
    
    # Формируем приветственное сообщение
    message = (
        f"👋 Привет, {user.first_name}!\n\n"
        "Я бот погоды, который поможет тебе узнать текущую погоду и прогноз "
        "на ближайшие дни в любом городе мира.\n\n"
        "Доступные команды:\n"
        "• /weather <город> - текущая погода\n"
        "• /forecast <город> - прогноз на 5 дней\n"
        "• /help - справка по командам\n\n"
        "Например, отправь мне: /weather Москва"
    )
    
    # Отправляем сообщение
    update.message.reply_text(message)