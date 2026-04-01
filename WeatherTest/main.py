import os
import sys

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from weather_data import CITY_DATA


class CityDropdownMenu(MDDropdownMenu):
    # фикс для меню городов

    def check_hor_growth(self) -> None:
        super().check_hor_growth()
        if not self.caller or not self.width:
            return
        cx, _ = self.caller.to_window(*self.caller.center)
        m = float(self.border_margin)
        if self.hor_growth == "left" and cx - self.width < m:
            self.hor_growth = "right"


class WeatherScreen(MDScreen):
    # класс экрана - всё что отображается при запуске

    # блок текущей погоды
    temperature = StringProperty("")
    city = StringProperty("")
    current_time_text = StringProperty("")
    weather_emoji = StringProperty("")
    emoji_font_name = StringProperty("")
    weather_status = StringProperty("")

    wind_text = StringProperty("")
    humidity_text = StringProperty("")

    # блок прогноза на день
    f1_temp = StringProperty("")
    f1_time = StringProperty("")
    f2_temp = StringProperty("")
    f2_time = StringProperty("")
    f3_temp = StringProperty("")
    f3_time = StringProperty("")
    f4_temp = StringProperty("")
    f4_time = StringProperty("")
    f1_emoji = StringProperty("")
    f2_emoji = StringProperty("")
    f3_emoji = StringProperty("")
    f4_emoji = StringProperty("")
    f1_icon = StringProperty("weather-partly-cloudy")
    f2_icon = StringProperty("weather-partly-cloudy")
    f3_icon = StringProperty("weather-partly-cloudy")
    f4_icon = StringProperty("weather-partly-cloudy")

    def update_weather(self):
        # функция "фейкового обновления страницы" по нажатию кнопки
        main_box = self.ids.main_box
        spinner = self.ids.spinner

        spinner.opacity = 1
        spinner.active = True

        anim_down = Animation(y=-90, d=0.25, t="out_quad")
        anim_up = Animation(y=0, d=0.25, t="out_quad")

        def after_down(*_):
            Clock.schedule_once(lambda *_: finish(), 1.0)

        def finish(*_):
            app = MDApp.get_running_app()
            if app:
                app.refresh_current_city_weather()
            anim_up.start(main_box)
            spinner.active = False
            spinner.opacity = 0

        anim_down.bind(on_complete=after_down)
        anim_down.start(main_box)


class WeatherApp(MDApp):
    # логика работы приложения

    def _detect_emoji_font(self) -> str:
        # ищем системный цветной шрифт с эмодзи для macOS/windows/linux чтобы заполнить поля
        candidates = []
        if sys.platform == "darwin":
            candidates = [
                "/System/Library/Fonts/Apple Color Emoji.ttc",
                "/System/Library/Fonts/Apple Symbols.ttf",
            ]
        elif sys.platform.startswith("win"):
            candidates = [
                "C:/Windows/Fonts/seguiemj.ttf",
                "C:/Windows/Fonts/seguisym.ttf",
            ]
        else:
            candidates = [
                "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            ]

        for font_path in candidates:
            if os.path.exists(font_path):
                return font_path
        return ""

    def build(self):
        # сборка окна, установка темы
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        root = Builder.load_file("weatherapp.kv")
        self.emoji_font_name = self._detect_emoji_font()
        # установка "дефолтных" значений
        self.city_time_is_12 = {city: False for city in CITY_DATA}
        self.selected_city = "Санкт-Петербург"
        Clock.schedule_once(lambda *_: self._apply_city("Санкт-Петербург"))
        return root

    def _apply_city(self, city: str) -> None:
        # добавление полей из CITY_DATA
        timeline = CITY_DATA.get(city)
        if not timeline:
            return

        is_12 = self.city_time_is_12.get(city, False)
        data = timeline.at_12 if is_12 else timeline.at_11

        screen: WeatherScreen = self.root
        screen.city = city
        screen.current_time_text = "12:00" if is_12 else "11:00"
        screen.emoji_font_name = self.emoji_font_name
        screen.temperature = data.temp_now
        screen.weather_emoji = data.emoji_now
        screen.weather_status = f"{data.condition_now}\n{data.feels_like}"
        screen.wind_text = data.wind
        screen.humidity_text = data.humidity

        points = data.day_forecast
        if len(points) >= 4:
            p1, p2, p3, p4 = points[:4]
            screen.f1_temp, screen.f1_time = p1.temp, p1.time
            screen.f2_temp, screen.f2_time = p2.temp, p2.time
            screen.f3_temp, screen.f3_time = p3.temp, p3.time
            screen.f4_temp, screen.f4_time = p4.temp, p4.time
            screen.f1_icon = p1.icon
            screen.f2_icon = p2.icon
            screen.f3_icon = p3.icon
            screen.f4_icon = p4.icon

    def open_city_menu(self):
        # основная функция выбора города из меню
        menu_items = [
            {"text": "Санкт-Петербург", "on_release": lambda x="Санкт-Петербург": self.set_city(x)},
            {"text": "Москва", "on_release": lambda x="Москва": self.set_city(x)},
            {"text": "Новосибирск", "on_release": lambda x="Новосибирск": self.set_city(x)},
        ]
        self.menu = CityDropdownMenu(
            caller=self.root.ids.city_button,
            items=menu_items,
            width=dp(240),
            position="bottom",
            border_margin=dp(12),
            ver_growth="down",
        )
        self.menu.open()

    def set_city(self, city):
        # выбор горда, перерисовка страницы, закрытие меню
        self.selected_city = city
        self._apply_city(city)
        if hasattr(self, "menu"):
            self.menu.dismiss()

    def refresh_current_city_weather(self) -> None:
        # отработка "фейкового обновления" по кнопке, переключение между 11:00 и 12:00
        city = self.selected_city
        if city not in CITY_DATA:
            return
        self.city_time_is_12[city] = not self.city_time_is_12.get(city, False)
        self._apply_city(city)


if __name__ == '__main__':
    WeatherApp().run()
