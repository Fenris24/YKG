import random
import time
import tkinter as tk
from tkinter import ttk

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

BG_COLOR = "#1e1e1e"
FG_COLOR = "#ffffff"
ENTRY_BG = "#2b2b2b"
ENTRY_FG = "#ffffff"
BTN_BG = "#ffffff"
BTN_FG = "#2e2d2d"
HINT_FG = "#cfcfcf"
OK_FG = "#00ff7f"
BAD_FG = "#ff4d4d"


class KanaGame:

    def __init__(self, master: tk.Tk) -> None:
        self.advance_locked = False

        self.master = master
        self.master.title("Yappanese Kana Racer")
        self.master.configure(bg=BG_COLOR)
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Two toggles (menu-only)
        self.include_hiragana_var = tk.BooleanVar(value=True)
        self.include_katakana_var = tk.BooleanVar(value=True)

        # Column selection toggles
        self.columns = {
            'a': tk.BooleanVar(value=True),
            'k': tk.BooleanVar(value=True),
            's': tk.BooleanVar(value=True),
            't': tk.BooleanVar(value=True),
            'n': tk.BooleanVar(value=True),
            'h': tk.BooleanVar(value=True),
            'm': tk.BooleanVar(value=True),
            'y': tk.BooleanVar(value=True),
            'r': tk.BooleanVar(value=True),
            'w': tk.BooleanVar(value=True),
        }
        self.include_n_var = tk.BooleanVar(value=True)
        self.include_dakuten_var = tk.BooleanVar(value=True)
        self.include_handakuten_var = tk.BooleanVar(value=True)

        self.start_time = None
        self.timer_after_id = None
        self.clear_timer_id = None

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

        self.start_frame = tk.Frame(master, bg=BG_COLOR)
        self.game_frame = tk.Frame(master, bg=BG_COLOR)
        self.result_frame = tk.Frame(master, bg=BG_COLOR)

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
        self.exit_dialog = None

        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
        self.style.configure("TCheckbutton", background=BG_COLOR, foreground=FG_COLOR)

        self.setup_start_screen()

    @staticmethod
    def _is_katakana(ch: str) -> bool:
        return 'ァ' <= ch <= 'ヿ'

    @staticmethod
    def _is_hiragana(ch: str) -> bool:
        return 'ぁ' <= ch <= 'ゟ'

    def _get_column(self, romaji: str) -> str | None:
        """Return the column name for a given romaji (e.g., 'k', 's', 'n'), or None."""
        if romaji in ('a', 'i', 'u', 'e', 'o'):
            return 'a'
        elif romaji.startswith('ka') or romaji.startswith('ki') or romaji.startswith('ku') or romaji.startswith('ke') or romaji.startswith('ko') or romaji.startswith('ga') or romaji.startswith('gi') or romaji.startswith('gu') or romaji.startswith('ge') or romaji.startswith('go'):
            return 'k'
        elif romaji.startswith('sa') or romaji.startswith('shi') or romaji.startswith('su') or romaji.startswith('se') or romaji.startswith('so') or romaji.startswith('za') or romaji.startswith('ji') or romaji.startswith('zu') or romaji.startswith('ze') or romaji.startswith('zo'):
            return 's'
        elif romaji.startswith('ta') or romaji.startswith('chi') or romaji.startswith('tsu') or romaji.startswith('te') or romaji.startswith('to') or romaji.startswith('da') or romaji.startswith('de') or romaji.startswith('do'):
            return 't'
        elif romaji.startswith('na') or romaji.startswith('ni') or romaji.startswith('nu') or romaji.startswith('ne') or romaji.startswith('no'):
            return 'n'
        elif romaji.startswith('ha') or romaji.startswith('hi') or romaji.startswith('fu') or romaji.startswith('he') or romaji.startswith('ho') or romaji.startswith('ba') or romaji.startswith('bi') or romaji.startswith('bu') or romaji.startswith('be') or romaji.startswith('bo') or romaji.startswith('pa') or romaji.startswith('pi') or romaji.startswith('pu') or romaji.startswith('pe') or romaji.startswith('po'):
            return 'h'
        elif romaji.startswith('ma') or romaji.startswith('mi') or romaji.startswith('mu') or romaji.startswith('me') or romaji.startswith('mo'):
            return 'm'
        elif romaji.startswith('ya') or romaji.startswith('yu') or romaji.startswith('yo'):
            return 'y'
        elif romaji.startswith('ra') or romaji.startswith('ri') or romaji.startswith('ru') or romaji.startswith('re') or romaji.startswith('ro'):
            return 'r'
        elif romaji.startswith('wa') or romaji.startswith('wo'):
            return 'w'
        elif romaji == 'n':
            return 'nn'
        return None

    def build_deck(self) -> None:
        include_hiragana = self.include_hiragana_var.get()
        include_katakana = self.include_katakana_var.get()
        include_dakuten = self.include_dakuten_var.get()
        include_handakuten = self.include_handakuten_var.get()

        items = []
        for ch, romaji in self.kana_romaji.items():
            # Check if character type is enabled
            if include_hiragana and self._is_hiragana(ch):
                pass
            elif include_katakana and self._is_katakana(ch):
                pass
            else:
                continue

            # Check if column is enabled
            column = self._get_column(romaji)
            if column is None:
                continue
            
            if column == 'nn':
                if not self.include_n_var.get():
                    continue
            else:
                if not self.columns[column].get():
                    continue

            # Dakuten / handakuten filters
            if romaji.startswith(('ga', 'gi', 'gu', 'ge', 'go', 'za', 'ji', 'zu', 'ze', 'zo', 'da', 'de', 'do', 'ba', 'bi', 'bu', 'be', 'bo')):
                if not include_dakuten:
                    continue
            elif romaji.startswith(('pa', 'pi', 'pu', 'pe', 'po')):
                if not include_handakuten:
                    continue

            items.append((ch, romaji))

        random.shuffle(items)
        self.kana_list = items

        self.current_index = 0
        self.wrong_flags = {char: False for char, _ in self.kana_list}
        self.hint_flags = {char: False for char, _ in self.kana_list}

    def open_column_menu(self) -> None:
        """Open a dialog to select columns and 'n'."""
        dialog = tk.Toplevel(self.master)
        dialog.title("Select Columns")
        dialog.geometry("400x600")
        dialog.configure(bg=BG_COLOR)

        tk.Label(
            dialog,
            text="Select Columns to Practice:",
            font=("Helvetica", 12, "bold"),
            bg=BG_COLOR,
            fg=FG_COLOR
        ).pack(pady=20)

        columns_frame = tk.Frame(dialog, bg=BG_COLOR)
        columns_frame.pack(pady=10)

        # Column display names
        column_names = {
            'a': 'A (あ・ア)',
            'k': 'K (か・カ)',
            's': 'S (さ・サ)',
            't': 'T (た・タ)',
            'n': 'N (な・ナ)',
            'h': 'H (は・ハ)',
            'm': 'M (ま・マ)',
            'y': 'Y (や・ヤ)',
            'r': 'R (ら・ラ)',
            'w': 'W (わ・ワ)',
            'nn': 'N (ん・ン)',
        }

        for col_key, col_name in column_names.items():
            ttk.Checkbutton(
                columns_frame,
                text=col_name,
                variable=self.columns[col_key] if col_key != 'nn' else self.include_n_var,
            ).pack(anchor="w", padx=10, pady=5)

        toggle_btn = tk.Button(
            dialog,
            text="",
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG,
            activeforeground=BTN_FG,
            highlightbackground=BG_COLOR,
        )
        toggle_btn.pack(pady=10)

        def update_toggle_btn_text(*args):
            try:
                all_selected = all(var.get() for var in self.columns.values()) and self.include_n_var.get()
                toggle_btn.config(text="Unselect All" if all_selected else "Select All")
            except:
                pass  # Button was destroyed when dialog closed

        def toggle_all():
            all_selected = all(var.get() for var in self.columns.values()) and self.include_n_var.get()
            new_state = not all_selected
            for var in self.columns.values():
                var.set(new_state)
            self.include_n_var.set(new_state)
            update_toggle_btn_text()

        # Add traces to update button text when checkboxes change
        for var in self.columns.values():
            var.trace_add('write', update_toggle_btn_text)
        self.include_n_var.trace_add('write', update_toggle_btn_text)

        toggle_btn.config(command=toggle_all)
        update_toggle_btn_text()

        # Dakuten / handakuten toggles (not affected by Select/Unselect All)
        toggles_frame = tk.Frame(dialog, bg=BG_COLOR)
        toggles_frame.pack(pady=(10, 10))

        ttk.Checkbutton(
            toggles_frame,
            text="Dakuten",
            variable=self.include_dakuten_var,
        ).pack(anchor="w", padx=10, pady=2)

        ttk.Checkbutton(
            toggles_frame,
            text="Handakuten",
            variable=self.include_handakuten_var,
        ).pack(anchor="w", padx=10, pady=2)

    def on_tab_hint(self, _event: tk.Event):
        self.show_hint()
        return "break"

    def on_key_press(self, event: tk.Event):
        """Handle key press - clear immediately if entry is red from wrong answer."""
        if self.entry is not None and str(self.entry.cget("fg")) == BAD_FG:
            # Cancel pending clear timer
            if self.clear_timer_id is not None:
                try:
                    self.master.after_cancel(self.clear_timer_id)
                except Exception:
                    pass
                self.clear_timer_id = None
            
            # Clear immediately and reset color
            if self.entry_var is not None:
                self.entry_var.set("")
            self.entry.configure(fg=ENTRY_FG)
        # Let the key event continue normally
        return None

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

        top_bar = tk.Frame(self.start_frame, bg=BG_COLOR)
        top_bar.pack(fill="x", pady=(0, 10))

        # Two toggles on the right
        toggles = tk.Frame(top_bar, bg=BG_COLOR)
        toggles.pack(side="right")

        ttk.Checkbutton(
            toggles,
            text="Hiragana",
            variable=self.include_hiragana_var,
        ).pack(side="left", padx=(0, 10))

        ttk.Checkbutton(
            toggles,
            text="Katakana",
            variable=self.include_katakana_var,
        ).pack(side="left")

        tk.Label(
            self.start_frame,
            text="Yappanese Kana Racer",
            font=("Helvetica", 24),
            bg=BG_COLOR,
            fg=FG_COLOR
        ).pack(pady=10)

        tk.Label(
            self.start_frame,
            text="Type the romaji for the shown kana.\nChoose a mode to begin.",
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=FG_COLOR
        ).pack(pady=(10, 4))

        # Message area for invalid selection (both toggles off)
        self.menu_msg = tk.Label(self.start_frame, text="", font=("Helvetica", 11), bg=BG_COLOR, fg=BAD_FG)
        self.menu_msg.pack(pady=(0, 10))

        tk.Button(
            self.start_frame,
            text="Classic Mode",
            width=20,
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG,
            activeforeground=BTN_FG,
            highlightbackground=BG_COLOR,
            command=lambda: self.start_game("classic")
        ).pack(pady=3)

        tk.Button(
            self.start_frame,
            text="Endless Mode",
            width=20,
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG,
            activeforeground=BTN_FG,
            highlightbackground=BG_COLOR,
            command=lambda: self.start_game("endless")
        ).pack(pady=3)

        tk.Button(
            self.start_frame,
            text="Select Columns",
            width=20,
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG,
            activeforeground=BTN_FG,
            highlightbackground=BG_COLOR,
            command=self.open_column_menu
        ).pack(pady=(14, 5))

    def start_game(self, mode: str) -> None:
        self.master.unbind("<Return>")
        # Must have at least one set enabled
        if not self.include_hiragana_var.get() and not self.include_katakana_var.get():
            if hasattr(self, "menu_msg") and self.menu_msg is not None:
                self.menu_msg.config(text="Enable Hiragana and/or Katakana to start.")
            return
        
        # Check if at least one column is selected
        any_column_selected = any(var.get() for var in self.columns.values()) or self.include_n_var.get()
        if not any_column_selected:
            if hasattr(self, "menu_msg") and self.menu_msg is not None:
                self.menu_msg.config(text="Select at least one column to practice.")
            return
        
        if hasattr(self, "menu_msg") and self.menu_msg is not None:
            self.menu_msg.config(text="")

        self.mode = mode
        self.build_deck()
        
        # Check if deck has characters
        if not self.kana_list:
            if hasattr(self, "menu_msg") and self.menu_msg is not None:
                self.menu_msg.config(text="No characters available with current selection.")
            return

        self.clear_frame(self.game_frame)
        self.start_frame.pack_forget()
        self.result_frame.pack_forget()
        self.game_frame.pack(padx=20, pady=20, fill="both", expand=True)

        top_bar = tk.Frame(self.game_frame, bg=BG_COLOR)
        top_bar.pack(fill="x", pady=(0, 10))

        left_box = tk.Frame(top_bar, bg=BG_COLOR)
        left_box.pack(side="left")

        self.progress_label = tk.Label(left_box, text="0/0", font=("Helvetica", 12), bg=BG_COLOR, fg=FG_COLOR)
        self.progress_label.pack(anchor="w")

        self.timer_label = tk.Label(left_box, text="00:00:00", font=("Helvetica", 12), bg=BG_COLOR, fg=FG_COLOR)
        self.timer_label.pack(anchor="w")

        self.char_label = tk.Label(self.game_frame, text="", font=("Helvetica", 72), pady=20, bg=BG_COLOR, fg=FG_COLOR)
        self.char_label.pack()

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            self.game_frame,
            textvariable=self.entry_var,
            font=("Helvetica", 20),
            width=15,
            bg=ENTRY_BG,
            fg=ENTRY_FG,
            insertbackground=ENTRY_FG,
        )
        self.entry.pack()
        self.entry.bind("<Return>", self.check_answer)
        self.entry.bind("<KeyPress>", self.on_key_press)

        self.entry.bind("<Tab>", self.on_tab_hint)
        self.master.bind("<Tab>", self.on_tab_hint)

        hint_row = tk.Frame(self.game_frame, bg=BG_COLOR)
        hint_row.pack(pady=10)

        self.hint_btn = tk.Button(
            hint_row,
            text="Hint",
            width=10,
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG,
            activeforeground=BTN_FG,
            highlightbackground=BG_COLOR,
            command=self.show_hint
        )
        self.hint_btn.pack(side="left", padx=(0, 10))

        self.hint_label = tk.Label(hint_row, text="", font=("Helvetica", 14), bg=BG_COLOR, fg=HINT_FG)
        self.hint_label.pack(side="left")

        self.feedback = tk.Label(self.game_frame, text="", font=("Helvetica", 14), bg=BG_COLOR, fg=FG_COLOR)
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
            self.entry.configure(fg=ENTRY_FG)
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
                self.entry.configure(fg=OK_FG)
                self.entry.unbind("<Return>")
            self.master.after(200, self.next_character)
        else:
            self.wrong_flags[char] = True
            if self.entry is not None:
                self.entry.configure(fg=BAD_FG)
            self.clear_timer_id = self.master.after(1000, self.clear_entry)

    def next_character(self) -> None:
        self.current_index += 1
        self.show_character()

    def clear_entry(self) -> None:
        self.clear_timer_id = None
        if self.entry_var is not None:
            self.entry_var.set("")
        if self.entry is not None:
            self.entry.configure(fg=ENTRY_FG)
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
            justify="center",
            bg=BG_COLOR,
            fg=FG_COLOR
        ).pack(pady=20)

        tk.Button(
            self.result_frame,
            text="Play Again",
            width=20,
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG,
            activeforeground=BTN_FG,
            highlightbackground=BG_COLOR,
            command=lambda: self.start_game(self.mode)
        ).pack(pady=5)

        tk.Button(
            self.result_frame,
            text="Main Menu",
            width=20,
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG,
            activeforeground=BTN_FG,
            highlightbackground=BG_COLOR,
            command=self.return_to_start
        ).pack(pady=5)

        self.result_frame.bind("<Return>", self._on_result_enter)
        self.result_frame.focus_set()

    def return_to_start(self) -> None:
        self.stop_timer()
        self.start_time = None

        self.result_frame.unbind("<Return>")

        self.result_frame.pack_forget()
        self.game_frame.pack_forget()
        self.mode = None
        self.setup_start_screen()

    def _on_result_enter(self, _event: tk.Event) -> None:
        self.start_game(self.mode)

    def on_close(self) -> None:
        """Handle window close button."""
        if self.result_frame.winfo_ismapped():
            # If on results screen, close the application
            self.master.destroy()
        elif self.game_frame.winfo_ismapped():
            # If in game, show custom menu dialog
            self.show_exit_menu()
        else:
            # If in main menu, close the application
            self.master.destroy()

    def show_exit_menu(self) -> None:
        """Show exit menu during game with Go to Menu and Quit options."""
        # If dialog already exists, focus on it
        if self.exit_dialog is not None and self.exit_dialog.winfo_exists():
            self.exit_dialog.focus_force()
            return
        
        dialog = tk.Toplevel(self.master)
        self.exit_dialog = dialog
        dialog.title("Exit Game")
        dialog.geometry("240x60")
        dialog.configure(bg=BG_COLOR)
        
        buttons_frame = tk.Frame(dialog, bg=BG_COLOR)
        buttons_frame.pack(padx=20, pady=(15, 5))
        
        def on_menu():
            self.exit_dialog = None
            dialog.destroy()
            self.return_to_start()
        
        def on_quit():
            self.exit_dialog = None
            dialog.destroy()
            self.master.destroy()
        
        def on_close():
            self.exit_dialog = None
            dialog.destroy()
        
        dialog.protocol("WM_DELETE_WINDOW", on_close)
        
        tk.Button(
            buttons_frame,
            text="Go to Menu",
            width=8,
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG,
            activeforeground=BTN_FG,
            highlightbackground=BG_COLOR,
            command=on_menu
        ).pack(side="left", padx=5)
        
        tk.Button(
            buttons_frame,
            text="Quit",
            width=8,
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG,
            activeforeground=BTN_FG,
            highlightbackground=BG_COLOR,
            command=on_quit
        ).pack(side="left", padx=5)

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
