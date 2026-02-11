from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    bg: str = "#0f0f10"
    panel: str = "#17181a"
    panel_border: str = "#2c2e32"
    text: str = "#f2f2f2"
    muted: str = "#c0c0c0"
    accent: str = "#f2f2f2"
    accent_dark: str = "#dedede"
    danger: str = "#b0b0b0"


DEFAULT_THEME = Theme()


def stylesheet(theme: Theme = DEFAULT_THEME) -> str:
    return f"""
    QWidget {{
        background: {theme.bg};
        color: {theme.text};
        font-family: "Segoe UI", "Noto Sans", "Arial", sans-serif;
        font-size: 14px;
    }}

    QLabel#Title {{
        font-size: 26px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}

    QFrame#Card {{
        background: {theme.panel};
        border: 1px solid {theme.panel_border};
        border-radius: 16px;
        padding: 6px;
    }}

    QLabel {{
        color: {theme.text};
    }}

    QPushButton {{
        background: {theme.accent};
        color: #111111;
        border: none;
        border-radius: 10px;
        padding: 12px 16px;
        font-weight: 600;
        margin-top: 4px;
        margin-bottom: 4px;
    }}

    QPushButton:hover {{
        background: {theme.accent_dark};
    }}

    QPushButton:pressed {{
        background: {theme.accent_dark};
        padding-top: 11px;
        padding-bottom: 9px;
    }}

    QPushButton:disabled {{
        background: #3a3a3a;
        color: #888888;
    }}

    QCheckBox, QRadioButton {{
        color: {theme.text};
        spacing: 8px;
        padding: 2px 0px;
    }}

    QCheckBox::indicator, QRadioButton::indicator {{
        width: 16px;
        height: 16px;
    }}

    QCheckBox::indicator {{
        border-radius: 4px;
        border: 1px solid {theme.panel_border};
        background: #0f0f10;
    }}

    QCheckBox::indicator:checked {{
        background: {theme.accent};
        border: 1px solid {theme.accent_dark};
    }}

    QRadioButton::indicator {{
        border-radius: 8px;
        border: 1px solid {theme.panel_border};
        background: #0f0f10;
    }}

    QRadioButton::indicator:checked {{
        background: {theme.accent};
        border: 1px solid {theme.accent_dark};
    }}

    QScrollBar:vertical {{
        background: {theme.panel};
        width: 10px;
        margin: 6px 2px 6px 2px;
        border-radius: 5px;
    }}

    QScrollBar::handle:vertical {{
        background: {theme.panel_border};
        min-height: 20px;
        border-radius: 5px;
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    """.strip()


def apply_theme(app, theme: Theme = DEFAULT_THEME) -> None:
    app.setStyleSheet(stylesheet(theme))
