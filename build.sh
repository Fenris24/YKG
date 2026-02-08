#!/bin/sh

if [ "$(uname -s)" = "Darwin" ]; then
  pyinstaller --noconsole --name "Yappanese Kana Racer" --icon icon.icns hiragana_katakana_game.py
else
  echo "This script is intended for macOS (Darwin)."
  exit 1
fi
