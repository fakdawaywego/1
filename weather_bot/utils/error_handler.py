import html
import json
import traceback
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from config import logger

def error_handler(update: Update, context: CallbackContext) -> None:
    """
    Обрабатывает ошибки, возникающие при обработке сообщений
    
    Args:
        update: Объект с информацией о сообщении
        context: Контекст обработчика
    """
    # Записываем ошибку в лог
    logger.error(f"Произошла ошибка: {context.error}")
    
    # Получаем информацию об ошибке
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)
    
    # Формируем сообщение об ошибке для лога
    error_message = (
        f"Произошла ошибка при обработке запроса.\n"
        f"Ошибка: {context.error}"
    )
    
    # Записываем подробную информацию в лог
    logger.error(f"Трассировка ошибки:\n{tb_string}")
    
    # Если есть сообщение, отправляем пользователю уведомление об ошибке
    if update and update.effective_message:
        # Определяем тип ошибки и отправляем соответствующее сообщение
        if "ConnectionError" in tb_string or "Timeout" in tb_string:
            update.effective_message.reply_text(
                "😕 Не удалось подключиться к серверу погоды. "
                "Пожалуйста, попробуйте позже."
            )
        elif "InvalidToken" in tb_string:
            update.effective_message.reply_text(
                "⚠️ Ошибка конфигурации бота. "
                "Пожалуйста, сообщите администратору."
            )
        else:
            update.effective_message.reply_text(
                "😕 Произошла ошибка при обработке вашего запроса. "
                "Пожалуйста, попробуйте еще раз позже."
            )