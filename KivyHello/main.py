from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty

DEFAULT_WORD = "world"
WORD_DISPLAY_SECONDS = 2.0


class HelloApp(App):
    current_text = StringProperty("Hello, world!")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._prefix = "Hello, "
        self._suffix = "!"
        self._current_word = DEFAULT_WORD
        self._target_word = ""
        self._write_index = 0
        self._is_erasing = False
        self._ticker = None
        self._revert_clock = None

    def _format_line(self, word: str) -> str:
        return f"{self._prefix}{word}{self._suffix}"

    def build(self):
        return Builder.load_file("hello.kv")

    def _cancel_revert_timer(self):
        if self._revert_clock is not None:
            self._revert_clock.cancel()
            self._revert_clock = None

    def _cancel_animation(self):
        if self._ticker is not None:
            self._ticker.cancel()
            self._ticker = None

    def process_word(self):
        text_input = self.root.ids.text_input
        user_word = text_input.text.strip()
        if not user_word:
            return

        self._target_word = user_word
        text_input.text = ""

        self._cancel_revert_timer()
        self._cancel_animation()

        self._write_index = 0
        self._is_erasing = True
        self._ticker = Clock.schedule_interval(self._animate_text, 0.08)

    def _begin_revert_to_default(self, *_args):
        self._revert_clock = None
        self._cancel_animation()
        self._target_word = DEFAULT_WORD
        self._is_erasing = True
        self._write_index = 0
        self._ticker = Clock.schedule_interval(self._animate_text, 0.08)

    def _schedule_revert_after_delay(self):
        self._cancel_revert_timer()
        self._revert_clock = Clock.schedule_once(
            self._begin_revert_to_default, WORD_DISPLAY_SECONDS
        )

    def _animate_text(self, _dt):
        if self._is_erasing:
            if self._current_word:
                self._current_word = self._current_word[:-1]
                self.current_text = self._format_line(self._current_word)
                return True
            self._is_erasing = False

        if self._write_index < len(self._target_word):
            self._current_word += self._target_word[self._write_index]
            self.current_text = self._format_line(self._current_word)
            self._write_index += 1
            return True

        self._ticker = None
        if self._target_word != DEFAULT_WORD:
            self._schedule_revert_after_delay()
        return False


if __name__ == "__main__":
    HelloApp().run()
