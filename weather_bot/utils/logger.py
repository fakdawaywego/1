import logging
import os
from datetime import datetime

def setup_logger():
    """
    Настраивает логирование для бота
    
    Returns:
        Настроенный логгер
    """
    # Создаем директорию для логов, если она не существует
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Настраиваем формат логов
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Настраиваем логгер
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            # Вывод в консоль
            logging.StreamHandler(),
            # Запись в файл
            logging.FileHandler(
                f"logs/bot_{datetime.now().strftime('%Y-%m-%d')}.log",
                encoding='utf-8'
            )
        ]
    )
    
    # Получаем и возвращаем логгер
    logger = logging.getLogger('weather_bot')
    
    return logger