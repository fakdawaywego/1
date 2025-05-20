from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from config import TELEGRAM_TOKEN, logger
from handlers import start_command, help_command, weather_command, forecast_command, history_command
from handlers.message import text_message
from handlers.callback import button_callback
from utils.error_handler import error_handler

def main():
    """
    Основная функция для запуска бота
    """
    logger.info("Запуск бота...")
    
    # Создаем экземпляр Updater и передаем ему токен бота
    updater = Updater(TELEGRAM_TOKEN)
    
    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher
    
    # Регистрируем обработчики команд
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("weather", weather_command))
    dispatcher.add_handler(CommandHandler("forecast", forecast_command))
    dispatcher.add_handler(CommandHandler("history", history_command))
    
    # Регистрируем обработчик инлайн-кнопок
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    
    # Регистрируем обработчик текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_message))
    
    # Регистрируем обработчик ошибок
    dispatcher.add_error_handler(error_handler)
    
    # Запускаем бота
    updater.start_polling()
    logger.info("Бот запущен")
    
    # Останавливаем бота при нажатии Ctrl+C
    updater.idle()
    logger.info("Бот остановлен")

if __name__ == '__main__':
    main()
