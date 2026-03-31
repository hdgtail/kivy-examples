from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.slider import MDSlider
import os
import sys
import traceback
import tempfile
from datetime import datetime


class DemoScrollView(ScrollView):
    def _iter_descendants(self):
        stack = list(self.children)
        while stack:
            w = stack.pop()
            yield w
            stack.extend(getattr(w, "children", []))

    def _touch_is_on_mdslider(self, touch):
        x, y = touch.pos
        for w in self._iter_descendants():
            if isinstance(w, MDSlider) and w.collide_point(x, y):
                return True
        return False

    def on_touch_down(self, touch):
        if self._touch_is_on_mdslider(touch):
            return False
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self._touch_is_on_mdslider(touch):
            return False
        return super().on_touch_move(touch)


Factory.register("DemoScrollView", DemoScrollView)

_ERR_LOG_PATH = os.path.join(tempfile.gettempdir(), "KivyMDdemo_crash.log")

def _write_exception_log(prefix: str, exc: BaseException | None = None) -> None:
    try:
        with open(_ERR_LOG_PATH, "a", encoding="utf-8") as f:
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"{datetime.now().isoformat(timespec='seconds')} {prefix}\n")
            f.write(f"frozen={getattr(sys, 'frozen', False)}\n")
            f.write(f"executable={sys.executable}\n")
            f.write(f"cwd={os.getcwd()}\n")
            f.write(f"_MEIPASS={getattr(sys, '_MEIPASS', None)}\n")
            if exc is not None:
                f.write(f"exception={type(exc).__name__}: {exc}\n")
            f.write("traceback:\n")
            f.write(traceback.format_exc())
            f.write("\n")
    except Exception:
        pass


def _excepthook(exctype, value, tb) -> None:
    _write_exception_log("uncaught", value)
    return sys.__excepthook__(exctype, value, tb)


sys.excepthook = _excepthook


class KivyMDDemoApp(MDApp):
    slider_value = NumericProperty(40)
    slider_value_text = StringProperty("40")
    switch_state_text = StringProperty("OFF")
    checkbox_state_text = StringProperty("Не отмечено")
    action_text = StringProperty("Статус: готово к взаимодействию")

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        try:
            kv_candidates = []
            if getattr(sys, "frozen", False):
                base_dir = getattr(sys, "_MEIPASS", None)
                if base_dir:
                    kv_candidates.append(os.path.join(base_dir, "material.kv"))
                kv_candidates.append(os.path.join(os.path.dirname(sys.executable), "material.kv"))
                kv_candidates.append(os.path.join(os.path.dirname(__file__), "material.kv"))
            else:
                kv_candidates.append(os.path.join(os.path.dirname(__file__), "material.kv"))

            kv_path = next((p for p in kv_candidates if os.path.exists(p)), None)
            if not kv_path:
                raise FileNotFoundError(f"material.kv not found in candidates: {kv_candidates}")
            return Builder.load_file(kv_path)
        except Exception:
            _write_exception_log("build() failed")
            raise

    def on_slider_value(self, *args):
        value = args[-1] if args else self.slider_value
        self.slider_value = int(float(value))
        self.slider_value_text = str(self.slider_value)
        self.set_action(f"Слайдер: {self.slider_value_text}")

    def on_switch_active(self, *args):
        is_active = bool(args[-1]) if args else False
        self.switch_state_text = "ON" if is_active else "OFF"
        self.set_action(f"MDSwitch: {self.switch_state_text}")

    def on_checkbox_active(self, *args):
        is_active = bool(args[-1]) if args else False
        self.checkbox_state_text = "Отмечено" if is_active else "Не отмечено"
        self.set_action(f"MDCheckbox: {self.checkbox_state_text}")

    def set_action(self, text):
        self.action_text = f"Статус: {text}"


if __name__ == "__main__":
    KivyMDDemoApp().run()
    
