from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from ui.kana_guesser.kana_game_view import GameResults


class ResultsView(QWidget):
    play_again_clicked = Signal()
    kana_menu_clicked = Signal()

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

        title = QLabel("Results")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignHCenter)
        card_layout.addWidget(title)

        self.summary_label = QLabel("")
        self.summary_label.setAlignment(Qt.AlignHCenter)
        self.summary_label.setWordWrap(True)
        card_layout.addWidget(self.summary_label)

        self.details_label = QLabel("")
        self.details_label.setAlignment(Qt.AlignHCenter)
        self.details_label.setWordWrap(True)
        card_layout.addWidget(self.details_label)

        self.play_again_btn = QPushButton("Play again")
        self.main_menu_btn = QPushButton("Kana menu")

        card_layout.addWidget(self.play_again_btn)
        card_layout.addWidget(self.main_menu_btn)

        root.addStretch(1)
        root.addWidget(card)
        root.addStretch(1)

    def _connect_signals(self) -> None:
        self.play_again_btn.clicked.connect(self.play_again_clicked.emit)
        self.main_menu_btn.clicked.connect(self.kana_menu_clicked.emit)

    def set_results(self, results: GameResults) -> None:
        if results.completed and results.wrong_count == 0 and results.hint_count == 0:
            summary = "SUGOI! You answered everything first try."
        else:
            summary = "Game over!"

        details = [
            f"Completed: {'Yes' if results.completed else 'No'}",
            f"Time: {results.elapsed_str}",
            f"Retries needed: {results.wrong_count}",
            f"Hints used: {results.hint_count}",
        ]

        self.summary_label.setText(summary)
        self.details_label.setText("\n".join(details))
