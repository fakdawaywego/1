from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext
from services.geocoding import get_coordinates
from services.weather import get_weather
from utils.formatters import format_current_weather
from utils.keyboards import get_weather_actions_keyboard
from utils.history import save_request_to_history
from config import logger

# Список популярных городов для быстрого выбора
POPULAR_CITIES = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань"]

def weather_command(update: Update, context: CallbackContext) -> None:
    """
    Обрабатывает команду /weather
    
    Args:
        update: Объект с информацией о сообщении
        context: Контекст обработчика
    """
    user = update.effective_user
    
    # Получаем аргументы команды (название города)
    args = context.args
    
    if not args:
        # Если город не указан, предлагаем выбрать из популярных или ввести свой
        keyboard = [POPULAR_CITIES[i:i+2] for i in range(0, len(POPULAR_CITIES), 2)]
        keyboard.append(["Отмена"])
        
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True,
            resize_keyboard=True
        )
        
        update.message.reply_text(
            "Пожалуйста, выберите город из списка или введите название города:",
            reply_markup=reply_markup
        )
        
        # Устанавливаем состояние ожидания ввода города
        context.user_data["waiting_for_city"] = "weather"
        return
    
    # Объединяем аргументы в название города
    city = ' '.join(args)
    
    # Получаем погоду для указанного города
    get_weather_for_city(update, context, city)

def get_weather_for_city(update: Update, context: CallbackContext, city: str) -> None:
    """
    Получает и отправляет информацию о погоде для указанного города
    
    Args:
        update: Объект с информацией о сообщении
        context: Контекст обработчика
        city: Название города
    """
    user = update.effective_user
    logger.info(f"Пользователь {user.id} запросил погоду для города: {city}")
    
    # Сохраняем запрос в историю
    save_request_to_history(
        user_id=user.id,
        user_name=user.first_name,
        city=city,
        request_type="weather"
    )
    
    # Отправляем сообщение о начале обработки запроса
    message = update.message.reply_text(f"🔍 Получение погоды для города {city}...")
    
    # Получаем координаты города
    location = get_coordinates(city)
    
    if not location:
        message.edit_text(
            f"😕 Не удалось найти город '{city}'.\n"
            "Пожалуйста, проверьте название города и попробуйте снова."
        )
        return
    
    # Получаем данные о погоде
    weather_data = get_weather(location["latitude"], location["longitude"])
    
    if not weather_data:
        message.edit_text(
            f"😕 Не удалось получить данные о погоде для города {city}.\n"
            "Пожалуйста, попробуйте позже."
        )
        return
    
    # Форматируем ответ
    weather_text = format_current_weather(weather_data, location["display_name"])
    
    # Создаем инлайн-клавиатуру с действиями
    reply_markup = get_weather_actions_keyboard(city)
    
    # Отправляем сообщение с клавиатурой
    message.edit_text(
        weather_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    
    # Если использовалась клавиатура, убираем её
    if context.user_data.get("waiting_for_city"):
        update.message.reply_text(
            "Вы можете запросить погоду для другого города с помощью команды /weather <город>",
            reply_markup=ReplyKeyboardRemove()
        )
        # Сбрасываем состояние ожидания
        context.user_data.pop("waiting_for_city", None)