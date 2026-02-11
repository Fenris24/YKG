from __future__ import annotations

from dataclasses import dataclass
import random
import time
from typing import Optional

from PySide6.QtCore import Qt, QTimer, Signal, QEvent
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.kana_guesser.kana_menu import KanaOptions, KanaMode, TimerSpeed


@dataclass(frozen=True)
class GameResults:
    total: int
    wrong_count: int
    hint_count: int
    elapsed_str: str
    completed: bool


class KanaGameView(QWidget):
    game_finished = Signal(object)
    exit_clicked = Signal()

    OK_COLOR = "#00d455"
    BAD_COLOR = "#ff6b6b"
    ENTRY_TEXT = "#111111"
    ENTRY_BG = "#f8f8f8"
    ENTRY_BORDER = "#2c2e32"

    kana_romaji = {
        'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
        'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
        'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
        'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
        'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
        'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
        'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
        'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
        'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
        'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
        'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
        'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
        'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
        'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
        'わ': 'wa', 'を': 'wo', 'ん': 'n',

        'ア': 'a', 'イ': 'i', 'ウ': 'u', 'エ': 'e', 'オ': 'o',
        'カ': 'ka', 'キ': 'ki', 'ク': 'ku', 'ケ': 'ke', 'コ': 'ko',
        'ガ': 'ga', 'ギ': 'gi', 'グ': 'gu', 'ゲ': 'ge', 'ゴ': 'go',
        'サ': 'sa', 'シ': 'shi', 'ス': 'su', 'セ': 'se', 'ソ': 'so',
        'ザ': 'za', 'ジ': 'ji', 'ズ': 'zu', 'ゼ': 'ze', 'ゾ': 'zo',
        'タ': 'ta', 'チ': 'chi', 'ツ': 'tsu', 'テ': 'te', 'ト': 'to',
        'ダ': 'da', 'ヂ': 'ji', 'ヅ': 'zu', 'デ': 'de', 'ド': 'do',
        'ナ': 'na', 'ニ': 'ni', 'ヌ': 'nu', 'ネ': 'ne', 'ノ': 'no',
        'ハ': 'ha', 'ヒ': 'hi', 'フ': 'fu', 'ヘ': 'he', 'ホ': 'ho',
        'バ': 'ba', 'ビ': 'bi', 'ブ': 'bu', 'ベ': 'be', 'ボ': 'bo',
        'パ': 'pa', 'ピ': 'pi', 'プ': 'pu', 'ペ': 'pe', 'ポ': 'po',
        'マ': 'ma', 'ミ': 'mi', 'ム': 'mu', 'メ': 'me', 'モ': 'mo',
        'ヤ': 'ya', 'ユ': 'yu', 'ヨ': 'yo',
        'ラ': 'ra', 'リ': 'ri', 'ル': 'ru', 'レ': 're', 'ロ': 'ro',
        'ワ': 'wa', 'ヲ': 'wo', 'ン': 'n',
    }

    def __init__(self) -> None:
        super().__init__()

        self.opts = KanaOptions()
        self.kana_list: list[tuple[str, str]] = []
        self.current_index = 0
        self.wrong_flags: dict[str, bool] = {}
        self.hint_flags: dict[str, bool] = {}
        self.advance_locked = False
        self.last_char: Optional[str] = None

        self.start_time: Optional[float] = None
        self.game_over = False

        self.run_timer = QTimer(self)
        self.run_timer.timeout.connect(self._update_timer)

        self.death_timer = QTimer(self)
        self.death_timer.timeout.connect(self._update_death_timer)
        self.death_total_ms = 0
        self.death_remaining_ms = 0
        self.death_last_tick: Optional[float] = None

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(22, 22, 22, 22)
        card_layout.setSpacing(12)

        title = QLabel("Kana Racer")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignHCenter)
        card_layout.addWidget(title)

        top_row = QHBoxLayout()
        top_row.setSpacing(10)
        self.progress_label = QLabel("Left: 0")
        self.timer_label = QLabel("Time 00:00:00")
        top_row.addWidget(self.progress_label, 0, Qt.AlignLeft)
        top_row.addStretch(1)
        top_row.addWidget(self.timer_label, 0, Qt.AlignRight)
        card_layout.addLayout(top_row)

        self.char_label = QLabel("")
        self.char_label.setAlignment(Qt.AlignHCenter)
        self.char_label.setStyleSheet("font-size: 72px; font-weight: 600;")
        card_layout.addWidget(self.char_label)

        self.entry = QLineEdit()
        self.entry.setAlignment(Qt.AlignHCenter)
        self.entry.setMaxLength(16)
        self.entry.setFixedWidth(240)
        self.entry.setFixedHeight(40)
        self._set_entry_style(self.ENTRY_TEXT)
        self.death_timer_label = QLabel("")
        self.death_timer_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.death_timer_label.setStyleSheet("font-size: 22px; font-weight: 700;")
        self.death_timer_label.setFixedWidth(70)
        entry_row = QHBoxLayout()
        entry_row.addStretch(1)
        entry_row.addWidget(self.entry)
        entry_row.addSpacing(12)
        entry_row.addWidget(self.death_timer_label)
        entry_row.addStretch(1)
        card_layout.addLayout(entry_row)

        self.hint_row = QHBoxLayout()
        self.hint_btn = QPushButton("Hint")
        self.hint_btn.setFixedWidth(110)
        self.hint_label = QLabel("")
        self.hint_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.hint_label.setFixedWidth(180)
        self.hint_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.hint_row.addStretch(1)
        self.hint_row.addWidget(self.hint_btn, 0)
        self.hint_row.addSpacing(10)
        self.hint_row.addWidget(self.hint_label, 0)
        self.hint_row.addStretch(1)
        card_layout.addLayout(self.hint_row)

        end_row = QHBoxLayout()
        self.exit_btn = QPushButton("Exit")
        self.exit_btn.setFixedWidth(140)
        end_row.addStretch(1)
        end_row.addWidget(self.exit_btn)
        end_row.addStretch(1)
        card_layout.addLayout(end_row)

        root.addStretch(1)
        root.addWidget(card)
        root.addStretch(1)

    def _connect_signals(self) -> None:
        self.entry.returnPressed.connect(self._check_answer)
        self.hint_btn.clicked.connect(self._show_hint)
        self.exit_btn.clicked.connect(self._exit_to_menu)
        self.entry.installEventFilter(self)
        self.installEventFilter(self)

    def start_game(self, options: KanaOptions) -> None:
        self.opts = options
        self._apply_options()
        self._build_deck()
        self._reset_state()
        self._start_run_timer()
        self._show_character()

    def _apply_options(self) -> None:
        if self.opts.no_help:
            self.hint_btn.setEnabled(False)
            self.hint_label.setText("")
            self.hint_btn.setVisible(False)
            self.hint_label.setVisible(False)
        else:
            self.hint_btn.setVisible(True)
            self.hint_label.setVisible(True)

        self.progress_label.setVisible(not self.opts.endless)
        self.timer_label.setVisible(not self.opts.endless)
        self.death_timer_label.setVisible(self.opts.timer)

    @staticmethod
    def _is_katakana(ch: str) -> bool:
        return 'ァ' <= ch <= 'ヿ'

    @staticmethod
    def _is_hiragana(ch: str) -> bool:
        return 'ぁ' <= ch <= 'ゟ'

    def _build_deck(self) -> None:
        items: list[tuple[str, str]] = []

        for ch, romaji in self.kana_romaji.items():
            if self.opts.kana_mode is KanaMode.BOTH:
                items.append((ch, romaji))
            elif self.opts.kana_mode is KanaMode.HIRAGANA and self._is_hiragana(ch):
                items.append((ch, romaji))
            elif self.opts.kana_mode is KanaMode.KATAKANA and self._is_katakana(ch):
                items.append((ch, romaji))

        random.shuffle(items)
        if self.last_char and items and items[0][0] == self.last_char:
            for i in range(1, len(items)):
                if items[i][0] != self.last_char:
                    items[0], items[i] = items[i], items[0]
                    break
        self.kana_list = items
        self.current_index = 0
        self.wrong_flags = {char: False for char, _ in self.kana_list}
        self.hint_flags = {char: False for char, _ in self.kana_list}

    def _reset_state(self) -> None:
        self.advance_locked = False
        self.game_over = False
        self.start_time = None
        self.last_char = None
        self.run_timer.stop()
        self.death_timer.stop()
        self.timer_label.setText("Time 00:00:00")
        self.death_timer_label.setText("")
        self.entry.setText("")
        self._set_entry_style(self.ENTRY_TEXT)
        # feedback label removed for cleaner layout

    def _start_run_timer(self) -> None:
        if self.opts.endless:
            self.start_time = None
            self.run_timer.stop()
            return
        self.start_time = time.perf_counter()
        self.run_timer.start(10)

    def _update_timer(self) -> None:
        if self.start_time is None:
            return
        elapsed = time.perf_counter() - self.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        centis = int(elapsed * 100) % 100
        self.timer_label.setText(f"Time {minutes:02d}:{seconds:02d}:{centis:02d}")

    def _elapsed_str(self) -> str:
        if self.start_time is None:
            return "N/A"
        elapsed = time.perf_counter() - self.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        centis = int(elapsed * 100) % 100
        return f"{minutes:02d}:{seconds:02d}:{centis:02d}"

    def _show_character(self) -> None:
        if not self.kana_list:
            self._build_deck()

        if self.current_index >= len(self.kana_list):
            if self.opts.endless:
                self._build_deck()
            else:
                self._end_game(completed=True)
                return

        total = len(self.kana_list)
        remaining = total - self.current_index
        if not self.opts.endless:
            self.progress_label.setText(f"Left: {remaining}")

        char, _ = self.kana_list[self.current_index]
        self.char_label.setText(char)
        self.last_char = char

        self.entry.setText("")
        self._set_entry_style(self.ENTRY_TEXT)
        self.entry.setFocus()

        self.hint_label.setText("")
        if not self.opts.no_help:
            self.hint_btn.setEnabled(True)

        self.advance_locked = False
        self._start_death_timer()

    def _show_hint(self) -> None:
        if self.opts.no_help or self.current_index >= len(self.kana_list):
            return
        char, romaji = self.kana_list[self.current_index]
        self.hint_flags[char] = True
        self.hint_label.setText(romaji)
        self.hint_btn.setEnabled(False)

    def _check_answer(self) -> None:
        if self.advance_locked or self.current_index >= len(self.kana_list):
            return

        char, romaji = self.kana_list[self.current_index]
        user_input = self.entry.text().strip().lower()
        if not user_input:
            return

        if user_input.endswith("'"):
            user_input = user_input[:-1]

        if user_input == romaji:
            self.advance_locked = True
            self.death_timer.stop()
            self._set_entry_style(self.OK_COLOR)
            QTimer.singleShot(200, self._next_character)
        else:
            self.wrong_flags[char] = True
            self._set_entry_style(self.BAD_COLOR)
            if self.opts.sudden_death:
                QTimer.singleShot(300, lambda: self._end_game(completed=False))
            else:
                QTimer.singleShot(800, self._clear_entry)

    def _next_character(self) -> None:
        self.current_index += 1
        self._show_character()

    def _clear_entry(self) -> None:
        self.entry.setText("")
        self._set_entry_style(self.ENTRY_TEXT)
        self.entry.setFocus()

    def _end_game(self, completed: bool) -> None:
        if self.game_over:
            return
        self.game_over = True
        self.run_timer.stop()
        self.death_timer.stop()
        total = len(self.kana_list)
        wrong_count = sum(self.wrong_flags.values())
        hint_count = sum(self.hint_flags.values())
        results = GameResults(
            total=total,
            wrong_count=wrong_count,
            hint_count=hint_count,
            elapsed_str=self._elapsed_str(),
            completed=completed,
        )
        self.game_finished.emit(results)

    def _set_entry_style(self, color: str) -> None:
        self.entry.setStyleSheet(
            "font-size: 22px; "
            f"background: {self.ENTRY_BG}; "
            f"color: {color}; "
            f"border: 1px solid {self.ENTRY_BORDER}; "
            "border-radius: 8px; "
            "padding: 6px 10px;"
        )

    def _start_death_timer(self) -> None:
        self.death_timer.stop()
        if not self.opts.timer:
            self.death_timer_label.setText("")
            return

        self.death_total_ms = 2000 if self.opts.timer_speed is TimerSpeed.FAST else 1000
        self.death_remaining_ms = self.death_total_ms
        self.death_last_tick = time.perf_counter()
        self._update_death_label()
        self.death_timer.start(50)

    def _update_death_timer(self) -> None:
        if self.death_last_tick is None:
            return
        now = time.perf_counter()
        delta_ms = int((now - self.death_last_tick) * 1000)
        self.death_last_tick = now
        self.death_remaining_ms = max(0, self.death_remaining_ms - delta_ms)
        self._update_death_label()
        if self.death_remaining_ms <= 0:
            self._end_game(completed=False)

    def _update_death_label(self) -> None:
        total_cs = int(self.death_remaining_ms / 10)
        seconds = total_cs // 100
        centis = total_cs % 100
        self.death_timer_label.setText(f"{seconds:02d}:{centis:02d}")

    def _exit_to_menu(self) -> None:
        if self.game_over:
            return
        self.game_over = True
        self.run_timer.stop()
        self.death_timer.stop()
        self.exit_clicked.emit()

    def eventFilter(self, watched, event):  # noqa: N802
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Tab:
                self._show_hint()
                return True
            if key == Qt.Key_Escape:
                self._exit_to_menu()
                return True
        return super().eventFilter(watched, event)
