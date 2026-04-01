from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class DayPoint:
    # ячейка прогноза на день
    temp: str
    condition: str
    time: str
    icon: str


@dataclass(frozen=True)
class CityWeather:
    # текущая погода в городе + прогноз на день для одного слоя данных
    temp_now: str
    condition_now: str
    emoji_now: str
    feels_like: str
    wind: str
    humidity: str
    day_forecast: List[DayPoint]


@dataclass(frozen=True)
class CityWeatherTimeline:
    # два варианта одного города для переключения по кнопке обновить.
    at_11: CityWeather
    at_12: CityWeather


# параметры разметки иконок/эмодзи
FORECAST_ICON_TO_EMOJI: Dict[str, str] = {
    "weather-partly-cloudy": "⛅",
    "weather-sunny": "☀️",
    "weather-cloudy": "☁️",
    "weather-rainy": "🌧️",
}


def forecast_icon_to_emoji(icon_name: str) -> str:
    # передача эмодзи по ключу иконки
    return FORECAST_ICON_TO_EMOJI.get(icon_name, "🌤️")


# поля городов
CITY_DATA: Dict[str, CityWeatherTimeline] = {
    "Санкт-Петербург": CityWeatherTimeline(
        at_11=CityWeather(
            temp_now="+20°",
            condition_now="Облачно",
            emoji_now="🌤️",
            feels_like="Ощущается как +19°",
            wind="5 м/с",
            humidity="62%",
            day_forecast=[
                DayPoint("+21°", "Переменная облачность", "13:00", "weather-partly-cloudy"),
                DayPoint("+23°", "Солнечно", "15:00", "weather-sunny"),
                DayPoint("+26°", "Ясно", "17:00", "weather-sunny"),
                DayPoint("+22°", "Облачно", "19:00", "weather-cloudy"),
            ],
        ),
        at_12=CityWeather(
            temp_now="+21°",
            condition_now="Небольшая облачность",
            emoji_now="🌤️",
            feels_like="Ощущается как +20°",
            wind="6 м/с",
            humidity="58%",
            day_forecast=[
                DayPoint("+22°", "Переменная облачность", "14:00", "weather-partly-cloudy"),
                DayPoint("+24°", "Солнечно", "16:00", "weather-sunny"),
                DayPoint("+25°", "Ясно", "18:00", "weather-sunny"),
                DayPoint("+21°", "Облачно", "20:00", "weather-cloudy"),
            ],
        ),
    ),
    "Москва": CityWeatherTimeline(
        at_11=CityWeather(
            temp_now="+17°",
            condition_now="Пасмурно",
            emoji_now="🌤️",
            feels_like="Ощущается как +16°",
            wind="4 м/с",
            humidity="70%",
            day_forecast=[
                DayPoint("+18°", "Облачно", "13:00", "weather-partly-cloudy"),
                DayPoint("+20°", "Солнечно", "15:00", "weather-sunny"),
                DayPoint("+21°", "Ясно", "17:00", "weather-sunny"),
                DayPoint("+19°", "Облачно", "19:00", "weather-cloudy"),
            ],
        ),
        at_12=CityWeather(
            temp_now="+18°",
            condition_now="Облачно",
            emoji_now="🌤️",
            feels_like="Ощущается как +17°",
            wind="5 м/с",
            humidity="66%",
            day_forecast=[
                DayPoint("+19°", "Облачно", "14:00", "weather-partly-cloudy"),
                DayPoint("+21°", "Солнечно", "16:00", "weather-sunny"),
                DayPoint("+22°", "Ясно", "18:00", "weather-sunny"),
                DayPoint("+20°", "Облачно", "20:00", "weather-cloudy"),
            ],
        ),
    ),
    "Новосибирск": CityWeatherTimeline(
        at_11=CityWeather(
            temp_now="+11°",
            condition_now="Дождь",
            emoji_now="🌧️",
            feels_like="Ощущается как +9°",
            wind="7 м/с",
            humidity="78%",
            day_forecast=[
                DayPoint("+12°", "Дождь", "13:00", "weather-rainy"),
                DayPoint("+11°", "Дождь", "15:00", "weather-rainy"),
                DayPoint("+10°", "Облачно", "17:00", "weather-cloudy"),
                DayPoint("+8°", "Облачно", "19:00", "weather-cloudy"),
            ],
        ),
        at_12=CityWeather(
            temp_now="+12°",
            condition_now="Небольшой дождь",
            emoji_now="🌦️",
            feels_like="Ощущается как +10°",
            wind="6 м/с",
            humidity="74%",
            day_forecast=[
                DayPoint("+13°", "Дождь", "14:00", "weather-rainy"),
                DayPoint("+12°", "Небольшой дождь", "16:00", "weather-rainy"),
                DayPoint("+11°", "Облачно", "18:00", "weather-cloudy"),
                DayPoint("+9°", "Облачно", "20:00", "weather-cloudy"),
            ],
        ),
    ),
}
