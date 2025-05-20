from weather_bot.services.geocoding import get_coordinates
from weather_bot.services.weather import get_weather

def test_geocoding():
    city = "Москва"
    print(f"Поиск координат для города: {city}")
    
    location = get_coordinates(city)
    if location:
        print(f"Найдено: {location['display_name']}")
        print(f"Координаты: {location['latitude']}, {location['longitude']}")
    else:
        print(f"Не удалось найти координаты для города {city}")
    
    return location

def test_weather_api(latitude, longitude):
    print(f"Получение погоды для координат: {latitude}, {longitude}")
    
    weather_data = get_weather(latitude, longitude)
    if weather_data:
        current = weather_data.get("current", {})
        print(f"Текущая температура: {current.get('temperature_2m')}°C")
        print(f"Влажность: {current.get('relative_humidity_2m')}%")
        print(f"Скорость ветра: {current.get('wind_speed_10m')} км/ч")
        print(f"Код погоды: {current.get('weather_code')}")
        
        daily = weather_data.get("daily", {})
        print("\nПрогноз на 5 дней:")
        for i in range(len(daily.get("time", []))):
            date = daily["time"][i]
            max_temp = daily["temperature_2m_max"][i]
            min_temp = daily["temperature_2m_min"][i]
            precip = daily["precipitation_sum"][i]
            weather_code = daily["weather_code"][i]
            print(f"{date}: {min_temp}°C - {max_temp}°C, осадки: {precip} мм, код погоды: {weather_code}")
    else:
        print("Не удалось получить данные о погоде")

if __name__ == "__main__":
    location = test_geocoding()
    if location:
        test_weather_api(location["latitude"], location["longitude"])