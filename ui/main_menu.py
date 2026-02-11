from __future__ import annotations

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QLabel, QPushButton, QFrame, QVBoxLayout, QWidget


class MainMenu(QWidget):
    kana_racer_clicked = Signal()
    exit_clicked = Signal()

    def __init__(self) -> None:
        super().__init__()

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
        card_layout.setSpacing(14)

        title = QLabel("Yappanese")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignHCenter)
        card_layout.addWidget(title)

        self.kana_racer_btn = QPushButton("Kana racer")
        self.exit_btn = QPushButton("Exit")

        card_layout.addWidget(self.kana_racer_btn)
        card_layout.addWidget(self.exit_btn)

        root.addStretch(1)
        root.addWidget(card)
        root.addStretch(1)

    def _connect_signals(self) -> None:
        self.kana_racer_btn.clicked.connect(self.kana_racer_clicked.emit)
        self.exit_btn.clicked.connect(self.exit_clicked.emit)
