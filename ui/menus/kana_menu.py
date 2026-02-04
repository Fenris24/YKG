from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame,
    QCheckBox, QButtonGroup, QRadioButton
)


class KanaMode(Enum):
    BOTH = "hira+kata"
    HIRAGANA = "hiragana"
    KATAKANA = "katakana"

    def next(self) -> "KanaMode":
        order = [KanaMode.BOTH, KanaMode.HIRAGANA, KanaMode.KATAKANA]
        return order[(order.index(self) + 1) % len(order)]

    def label(self) -> str:
        if self is KanaMode.BOTH:
            return "Hira+Kata"
        if self is KanaMode.HIRAGANA:
            return "Hiragana"
        return "Katakana"


class TimerSpeed(Enum):
    FAST = "fast"
    VERY_FAST = "very_fast"

    def label(self) -> str:
        return "Fast" if self is TimerSpeed.FAST else "Very fast"


@dataclass
class KanaOptions:
    kana_mode: KanaMode = KanaMode.BOTH
    endless: bool = False
    sudden_death: bool = False
    no_help: bool = False
    timer: bool = False
    timer_speed: TimerSpeed = TimerSpeed.FAST  # default preference when timer is enabled


class KanaMenu(QWidget):
    kana_clicked = Signal()
    kanji_clicked = Signal()
    back_clicked = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.opts = KanaOptions()

        self._build_ui()
        self._connect_signals()
        self._refresh_ui()

    # ---------------- UI construction ----------------
    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        # Card container
        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(22, 22, 22, 22)
        card_layout.setSpacing(14)

        # Header
        title = QLabel("Yappanese Kana Guesser")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignHCenter)
        card_layout.addWidget(title)

        subtitle = QLabel("Choose your mode and options.")
        subtitle.setAlignment(Qt.AlignHCenter)
        card_layout.addWidget(subtitle)

        # Content: left (mode buttons) + right (options)
        content = QHBoxLayout()
        content.setSpacing(18)

        # Left side
        left = QVBoxLayout()
        left.setSpacing(10)

        self.kana_btn = QPushButton("Kana guesser")
        self.kana_mode_btn = QPushButton(self.opts.kana_mode.label())

        kana_row = QHBoxLayout()
        kana_row.setSpacing(10)
        kana_row.addWidget(self.kana_btn, 1)
        kana_row.addWidget(self.kana_mode_btn, 0)

        self.kanji_btn = QPushButton("Kanji guesser")
        self.back_btn = QPushButton("Back")

        left.addLayout(kana_row)
        left.addWidget(self.kanji_btn)
        left.addWidget(self.back_btn)
        left.addStretch(1)

        # Right side (options)
        right = QVBoxLayout()
        right.setSpacing(8)

        opts_title = QLabel("Options")
        opts_title.setAlignment(Qt.AlignLeft)
        right.addWidget(opts_title)

        self.endless_cb = QCheckBox("Endless")
        self.sudden_death_cb = QCheckBox("Sudden death")
        self.no_help_cb = QCheckBox("No help")
        self.timer_cb = QCheckBox("Timer")

        right.addWidget(self.endless_cb)
        right.addWidget(self.sudden_death_cb)
        right.addWidget(self.no_help_cb)
        right.addWidget(self.timer_cb)

        # Timer speed (shown only when timer enabled)
        self.timer_speed_box = QFrame()
        timer_speed_layout = QVBoxLayout(self.timer_speed_box)
        timer_speed_layout.setContentsMargins(18, 4, 0, 0)
        timer_speed_layout.setSpacing(6)

        self.fast_rb = QRadioButton("Fast")
        self.very_fast_rb = QRadioButton("Very fast")

        self.timer_speed_group = QButtonGroup(self)
        self.timer_speed_group.setExclusive(True)
        self.timer_speed_group.addButton(self.fast_rb)
        self.timer_speed_group.addButton(self.very_fast_rb)

        timer_speed_layout.addWidget(self.fast_rb)
        timer_speed_layout.addWidget(self.very_fast_rb)

        right.addWidget(self.timer_speed_box)
        right.addStretch(1)

        # Compose
        content.addLayout(left, 3)
        content.addLayout(right, 2)
        card_layout.addLayout(content)

        root.addStretch(1)
        root.addWidget(card)
        root.addStretch(1)

    # ---------------- Wiring / behavior ----------------
    def _connect_signals(self) -> None:
        # Navigation signals
        self.kana_btn.clicked.connect(self.kana_clicked.emit)
        self.kanji_btn.clicked.connect(self.kanji_clicked.emit)
        self.back_btn.clicked.connect(self.back_clicked.emit)

        # Kana mode cycle button
        self.kana_mode_btn.clicked.connect(self._cycle_kana_mode)

        # Option toggles -> update model + UI
        self.endless_cb.toggled.connect(self._on_endless_toggled)
        self.sudden_death_cb.toggled.connect(self._on_sudden_death_toggled)
        self.no_help_cb.toggled.connect(self._on_no_help_toggled)
        self.timer_cb.toggled.connect(self._on_timer_toggled)

        # Timer speed radios -> update model
        self.fast_rb.toggled.connect(lambda on: on and self._set_timer_speed(TimerSpeed.FAST))
        self.very_fast_rb.toggled.connect(lambda on: on and self._set_timer_speed(TimerSpeed.VERY_FAST))

    def _refresh_ui(self) -> None:
        # Reflect model -> widgets (used after changes)
        self.kana_mode_btn.setText(self.opts.kana_mode.label())

        self.endless_cb.setChecked(self.opts.endless)
        self.sudden_death_cb.setChecked(self.opts.sudden_death)
        self.no_help_cb.setChecked(self.opts.no_help)
        self.timer_cb.setChecked(self.opts.timer)

        self.timer_speed_box.setVisible(self.opts.timer)
        if self.opts.timer:
            if self.opts.timer_speed is TimerSpeed.FAST:
                self.fast_rb.setChecked(True)
            else:
                self.very_fast_rb.setChecked(True)
        else:
            # When timer is off, no selection shown
            self.timer_speed_group.setExclusive(False)
            self.fast_rb.setChecked(False)
            self.very_fast_rb.setChecked(False)
            self.timer_speed_group.setExclusive(True)

    # ---------------- Handlers ----------------
    def _cycle_kana_mode(self) -> None:
        self.opts.kana_mode = self.opts.kana_mode.next()
        self.kana_mode_btn.setText(self.opts.kana_mode.label())

    def _on_endless_toggled(self, enabled: bool) -> None:
        self.opts.endless = enabled

    def _on_sudden_death_toggled(self, enabled: bool) -> None:
        self.opts.sudden_death = enabled

    def _on_no_help_toggled(self, enabled: bool) -> None:
        self.opts.no_help = enabled

    def _on_timer_toggled(self, enabled: bool) -> None:
        self.opts.timer = enabled
        self.timer_speed_box.setVisible(enabled)

        # If timer gets enabled and nothing selected yet, default to FAST
        if enabled:
            if not self.fast_rb.isChecked() and not self.very_fast_rb.isChecked():
                self.opts.timer_speed = TimerSpeed.FAST
                self.fast_rb.setChecked(True)
        else:
            # Clear visible selection when timer off (keep default in model if you want)
            self.timer_speed_group.setExclusive(False)
            self.fast_rb.setChecked(False)
            self.very_fast_rb.setChecked(False)
            self.timer_speed_group.setExclusive(True)

    def _set_timer_speed(self, speed: TimerSpeed) -> None:
        self.opts.timer_speed = speed

    # ---------------- Public API ----------------
    def options(self) -> KanaOptions:
        """Return current options model (copy if you prefer immutability)."""
        return self.opts