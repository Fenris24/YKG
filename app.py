from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication, QStackedWidget

from theme import apply_theme
from ui.main_menu import MainMenu
from ui.kana_guesser.kana_menu import KanaMenu
from ui.kana_guesser.kana_game_view import KanaGameView
from ui.kana_guesser.results_view import ResultsView


def main() -> int:
    app = QApplication(sys.argv)
    apply_theme(app)

    stack = QStackedWidget()

    main_menu = MainMenu()
    kana_menu = KanaMenu()
    kana_game = KanaGameView()
    results_view = ResultsView()

    stack.addWidget(main_menu)
    stack.addWidget(kana_menu)
    stack.addWidget(kana_game)
    stack.addWidget(results_view)
    stack.setCurrentWidget(main_menu)

    current_kana_options = {"value": None}

    def start_kana_game() -> None:
        current_kana_options["value"] = kana_menu.options()
        kana_game.start_game(current_kana_options["value"])
        stack.setCurrentWidget(kana_game)

    def restart_kana_game() -> None:
        if current_kana_options["value"] is None:
            current_kana_options["value"] = kana_menu.options()
        kana_game.start_game(current_kana_options["value"])
        stack.setCurrentWidget(kana_game)

    def show_results(results) -> None:
        results_view.set_results(results)
        stack.setCurrentWidget(results_view)

    main_menu.kana_racer_clicked.connect(lambda: stack.setCurrentWidget(kana_menu))
    main_menu.exit_clicked.connect(app.quit)
    kana_menu.back_clicked.connect(lambda: stack.setCurrentWidget(main_menu))
    kana_menu.kana_clicked.connect(start_kana_game)

    kana_game.game_finished.connect(show_results)
    kana_game.exit_clicked.connect(lambda: stack.setCurrentWidget(kana_menu))
    results_view.play_again_clicked.connect(restart_kana_game)
    results_view.kana_menu_clicked.connect(lambda: stack.setCurrentWidget(kana_menu))

    stack.setWindowTitle("YKG")
    stack.resize(760, 560)
    stack.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
