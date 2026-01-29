import random
import time
import tkinter as tk
from tkinter import ttk

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400


class KanaGame:

    def __init__(self, master: tk.Tk) -> None:

        self.advance_locked = False

        self.master = master
        self.master.title("Yappanese Kana Racer")

        self.include_katakana_var = tk.BooleanVar(value=True)

        self.start_time = None
        self.timer_after_id = None

        self.kana_romaji = {
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

        self.start_frame = tk.Frame(master)
        self.game_frame = tk.Frame(master)
        self.result_frame = tk.Frame(master)

        self.mode = None
        self.kana_list = []
        self.current_index = 0
        self.wrong_flags = {}
        self.hint_flags = {}

        self.progress_label = None
        self.timer_label = None
        self.char_label = None
        self.entry = None
        self.entry_var = None
        self.hint_btn = None
        self.hint_label = None
        self.feedback = None

        self.setup_start_screen()

    @staticmethod
    def _is_katakana(ch: str) -> bool:
        return 'ァ' <= ch <= 'ヿ'

    @staticmethod
    def _is_hiragana(ch: str) -> bool:
        return 'ぁ' <= ch <= 'ゟ'

    def build_deck(self) -> None:
        include_katakana = self.include_katakana_var.get()

        items = []
        for ch, romaji in self.kana_romaji.items():
            if self._is_hiragana(ch):
                items.append((ch, romaji))
            elif include_katakana and self._is_katakana(ch):
                items.append((ch, romaji))

        random.shuffle(items)
        self.kana_list = items

        self.current_index = 0
        self.wrong_flags = {char: False for char, _ in self.kana_list}
        self.hint_flags = {char: False for char, _ in self.kana_list}

    def on_tab_hint(self, _event: tk.Event):
        self.show_hint()
        return "break"

    def stop_timer(self):
        if self.timer_after_id is not None:
            try:
                self.master.after_cancel(self.timer_after_id)
            except Exception:
                pass
            self.timer_after_id = None

    def update_timer(self):
        if self.start_time is None or self.timer_label is None:
            return

        elapsed = time.perf_counter() - self.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        centis = int(elapsed * 100) % 100

        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}:{centis:02d}")
        self.timer_after_id = self.master.after(10, self.update_timer)

    def get_elapsed_str(self) -> str:
        if self.start_time is None:
            return "00:00:00"
        elapsed = time.perf_counter() - self.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        centis = int(elapsed * 100) % 100
        return f"{minutes:02d}:{seconds:02d}:{centis:02d}"


    def setup_start_screen(self) -> None:
        self.stop_timer()
        self.start_time = None

        self.clear_frame(self.start_frame)
        self.start_frame.pack(padx=20, pady=20, fill="both", expand=True)

        top_bar = tk.Frame(self.start_frame)
        top_bar.pack(fill="x", pady=(0, 10))

        self.katakana_toggle_start = ttk.Checkbutton(
            top_bar,
            text="Katakana",
            variable=self.include_katakana_var,
        )
        self.katakana_toggle_start.pack(side="right")

        tk.Label(self.start_frame, text="Yappanese Kana Racer", font=("Helvetica", 24)).pack(pady=10)

        tk.Label(
            self.start_frame,
            text="Type the romaji for the shown kana.\nChoose a mode to begin.",
            font=("Helvetica", 12),
        ).pack(pady=10)

        tk.Button(self.start_frame, text="Classic Mode", width=20,
                  command=lambda: self.start_game("classic")).pack(pady=5)

        tk.Button(self.start_frame, text="Endless Mode", width=20,
                  command=lambda: self.start_game("endless")).pack(pady=5)

        tk.Button(self.start_frame, text="Quit", width=20,
                  command=self.master.quit).pack(pady=5)

    def start_game(self, mode: str) -> None:
        self.mode = mode
        self.build_deck()

        self.clear_frame(self.game_frame)
        self.start_frame.pack_forget()
        self.result_frame.pack_forget()
        self.game_frame.pack(padx=20, pady=20, fill="both", expand=True)

        top_bar = tk.Frame(self.game_frame)
        top_bar.pack(fill="x", pady=(0, 10))

        left_box = tk.Frame(top_bar)
        left_box.pack(side="left")

        self.progress_label = tk.Label(left_box, text="0/0", font=("Helvetica", 12))
        self.progress_label.pack(anchor="w")

        self.timer_label = tk.Label(left_box, text="00:00:00", font=("Helvetica", 12))
        self.timer_label.pack(anchor="w")

        self.char_label = tk.Label(self.game_frame, text="", font=("Helvetica", 72), pady=20)
        self.char_label.pack()

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.game_frame, textvariable=self.entry_var, font=("Helvetica", 20), width=15)
        self.entry.pack()
        self.entry.bind("<Return>", self.check_answer)

        self.entry.bind("<Tab>", self.on_tab_hint)
        self.master.bind("<Tab>", self.on_tab_hint)

        hint_row = tk.Frame(self.game_frame)
        hint_row.pack(pady=10)

        self.hint_btn = tk.Button(hint_row, text="Hint", width=10, command=self.show_hint)
        self.hint_btn.pack(side="left", padx=(0, 10))

        self.hint_label = tk.Label(hint_row, text="", font=("Helvetica", 14))
        self.hint_label.pack(side="left")

        self.feedback = tk.Label(self.game_frame, text="", font=("Helvetica", 14))
        self.feedback.pack(pady=10)

        self.stop_timer()
        self.start_time = time.perf_counter()
        self.update_timer()

        self.show_character()

    def show_character(self) -> None:
        if not self.kana_list:
            self.build_deck()

        if self.current_index >= len(self.kana_list):
            if self.mode == "classic":
                self.end_game()
                return

            self.build_deck()

        total = len(self.kana_list)
        current_n = self.current_index + 1
        if self.progress_label is not None:
            self.progress_label.config(text=f"{current_n}/{total}")

        char, _ = self.kana_list[self.current_index]
        if self.char_label is not None:
            self.char_label.config(text=char)

        if self.entry_var is not None:
            self.entry_var.set("")
        if self.entry is not None:
            self.entry.configure(fg="black", state="normal")
            self.entry.focus_set()

        if self.feedback is not None:
            self.feedback.config(text="")
        if self.hint_label is not None:
            self.hint_label.config(text="")
        if self.hint_btn is not None:
            self.hint_btn.config(state="normal")

        self.advance_locked = False
        if self.entry is not None:
            self.entry.bind("<Return>", self.check_answer)

    def show_hint(self) -> None:
        if self.current_index >= len(self.kana_list):
            return
        char, romaji = self.kana_list[self.current_index]
        self.hint_flags[char] = True
        if self.hint_label is not None:
            self.hint_label.config(text=f"Hint: {romaji}")
        if self.hint_btn is not None:
            self.hint_btn.config(state="disabled")

    def check_answer(self, _event: tk.Event) -> None:

        if self.advance_locked:
            return

        if self.current_index >= len(self.kana_list):
            return

        char, romaji = self.kana_list[self.current_index]
        user_input = (self.entry_var.get() if self.entry_var is not None else "").strip().lower()

        if user_input.endswith("'"):
            user_input = user_input[:-1]

        if user_input == romaji:
            self.advance_locked = True
            if self.entry is not None:
                self.entry.configure(fg="green")
                self.entry.unbind("<Return>")
            self.master.after(200, self.next_character)
        else:
            self.wrong_flags[char] = True
            if self.entry is not None:
                self.entry.configure(fg="red")
            self.master.after(1000, self.clear_entry)

    def next_character(self) -> None:
        self.current_index += 1
        self.show_character()

    def clear_entry(self) -> None:
        if self.entry_var is not None:
            self.entry_var.set("")
        if self.entry is not None:
            self.entry.configure(fg="black")
            self.entry.focus_set()

    def end_game(self) -> None:
        final_time = self.get_elapsed_str()
        self.stop_timer()

        wrong_count = sum(self.wrong_flags.values())
        hint_count = sum(self.hint_flags.values())

        self.game_frame.pack_forget()
        self.clear_frame(self.result_frame)
        self.result_frame.pack(padx=20, pady=20, fill="both", expand=True)

        if wrong_count == 0 and hint_count == 0:
            result_msg = f"SUGOI! You answered everything first try.\nTime: {final_time}"
        else:
            result_msg = (
                f"Game over!\n"
                f"Time: {final_time}\n"
                f"Retries needed: {wrong_count}\n"
                f"Hints used: {hint_count}"
            )

        tk.Label(
            self.result_frame,
            text=result_msg,
            font=("Helvetica", 16),
            wraplength=420,
            justify="center"
        ).pack(pady=20)

        tk.Button(self.result_frame, text="Play Again", width=20,
                  command=lambda: self.start_game(self.mode)).pack(pady=5)

        tk.Button(self.result_frame, text="Main Menu", width=20,
                  command=self.return_to_start).pack(pady=5)

    def return_to_start(self) -> None:
        self.stop_timer()
        self.start_time = None

        self.result_frame.pack_forget()
        self.game_frame.pack_forget()
        self.mode = None
        self.setup_start_screen()

    @staticmethod
    def clear_frame(frame: tk.Frame) -> None:
        for widget in frame.winfo_children():
            widget.destroy()


def main() -> None:
    root = tk.Tk()
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    KanaGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
