from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_weather_actions_keyboard(city: str) -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру с действиями для погоды
    
    Args:
        city: Название города
        
    Returns:
        Инлайн-клавиатура с кнопками действий
    """
    keyboard = [
        [
            InlineKeyboardButton("Прогноз на 5 дней", callback_data=f"forecast_{city}")
        ],
        [
            InlineKeyboardButton("Обновить данные", callback_data=f"refresh_weather_{city}")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_forecast_actions_keyboard(city: str) -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру с действиями для прогноза
    
    Args:
        city: Название города
        
    Returns:
        Инлайн-клавиатура с кнопками действий
    """
    keyboard = [
        [
            InlineKeyboardButton("Текущая погода", callback_data=f"weather_{city}")
        ],
        [
            InlineKeyboardButton("Обновить данные", callback_data=f"refresh_forecast_{city}")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)