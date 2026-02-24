import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyautogui
from PIL import Image
import time
import threading
import easyocr
import pyperclip
import numpy as np
from openai import OpenAI

# ────────────────────────────────────────────────
#                 CONFIGURATION
# ────────────────────────────────────────────────

# Load API key from external file
try:
    with open("API-Key.txt", "r") as f:
        OPENROUTER_API_KEY = f.read().strip()
except FileNotFoundError:
    messagebox.showerror("Missing File", "API-Key.txt not found in the same folder.")
    exit()
except Exception as e:
    messagebox.showerror("Key Error", f"Could not read API-Key.txt:\n{e}")
    exit()

if not OPENROUTER_API_KEY:
    messagebox.showerror("Empty Key", "API-Key.txt is empty. Paste your key inside it.")
    exit()

# Load models from models.txt
try:
    with open("models.txt", "r") as f:
        FREE_MODELS = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    messagebox.showerror("Missing File", "models.txt not found in the same folder.\nCreate it with one model per line.")
    exit()
except Exception as e:
    messagebox.showerror("File Error", f"Could not read models.txt:\n{e}")
    exit()

if not FREE_MODELS:
    messagebox.showerror("Empty File", "models.txt is empty.\nAdd at least one model (e.g. qwen/qwen-2.5-7b-instruct:free)")
    exit()

READER_LANGUAGES = ['en']

AI_PROMPT = """You are solving a multiple-choice quiz question from raw screenshot text.
The text is messy OCR output (may include junk like browser tabs/bookmarks).

1. Identify the actual question (usually the longest/most sentence-like part).
2. Identify the answer options (usually 4 lines starting with A/B/C/D or 1/2/3/4).
3. Choose the correct answer.
4. Return ONLY one line:   <letter-or-number> <full text of the correct option>

Examples:
B Bonds
2 Photosynthesis
C The mitochondria is the powerhouse of the cell

If you cannot clearly identify question/options or pick an answer, return exactly: "Cannot determine answer"

Raw extracted text:
{raw_text}

Answer now:"""

# ────────────────────────────────────────────────

class QuizSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR API Quiz Bot")
        self.root.geometry("820x750")
        self.root.resizable(False, False)
        self.running = False
        self.spin_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        self.spin_index = 0
        try:
            self.reader = easyocr.Reader(READER_LANGUAGES, gpu=False)
        except Exception as e:
            messagebox.showerror("EasyOCR Error", str(e))
            root.destroy()
            return
        self.ai_client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )
        self.create_ui()

    def create_ui(self):
        pad = 16
        main = ttk.Frame(self.root, padding=pad)
        main.pack(fill=tk.BOTH, expand=True)
        self.btn = ttk.Button(
            main,
            text="Scan",
            command=self.start_process,
            style="Big.TButton"
        )
        self.btn.pack(pady=(pad, 20), ipadx=50, ipady=18)
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(main, textvariable=self.status_var, font=("Segoe UI", 11, "bold"))
        self.status_label.pack(pady=(0, 6))
        self.spin_var = tk.StringVar(value="")
        self.spin_label = ttk.Label(main, textvariable=self.spin_var, font=("Consolas", 18), foreground="#555")
        self.spin_label.pack(pady=(0, 12))
        ttk.Label(main, text="Detected Raw OCR:", font=("Segoe UI", 10)).pack(anchor="w")
        self.raw_text = scrolledtext.ScrolledText(main, wrap=tk.WORD, font=("Consolas", 11), height=8, state="disabled", bg="#f8f9fa")
        self.raw_text.pack(fill=tk.X, pady=(4, 12))
        ttk.Label(main, text="Answer Field:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.answer_text = scrolledtext.ScrolledText(main, wrap=tk.WORD, font=("Consolas", 14, "bold"), height=6, state="disabled", bg="#e8f5e9")
        self.answer_text.pack(fill=tk.X, pady=(4, 8))
        self.copy_btn = ttk.Button(main, text="Copy Answer Field", command=self.copy_answer, state="disabled")
        self.copy_btn.pack(pady=8)
        style = ttk.Style()
        style.configure("Big.TButton", font=("Segoe UI", 13, "bold"))

    def start_process(self):
        if self.running: return
        self.running = True
        self.btn.state(["disabled"])
        self.copy_btn.state(["disabled"])
        self._clear_all()
        threading.Thread(target=self._process, daemon=True).start()

    def _process(self):
        self._update_status("Preparing...", "blue")
        time.sleep(0.4)
        self._update_status("Capturing...", "dodgerblue")
        try:
            img_pil = pyautogui.screenshot()
            if img_pil.mode == "RGBA":
                img_pil = img_pil.convert("RGB")
            img = np.array(img_pil)
        except Exception as e:
            self._finish_error(f"Screenshot error:\n{e}")
            return
        self._update_status("OCR in progress...", "purple")
        self._start_spinner()
        try:
            ocr_result = self.reader.readtext(img, detail=0, paragraph=True)
            raw_text = "\n".join(line.strip() for line in ocr_result if line.strip() and len(line.strip()) > 2)
            if not raw_text:
                raw_text = "[No text detected]"
        except Exception as e:
            raw_text = f"OCR error:\n{str(e)}"
        self._set_text(self.raw_text, raw_text)
        self._update_status("Asking AI models...", "indigo")
        ai_answer = "[All models failed - check key & internet]"
        used_model = "None"
        for model in FREE_MODELS:
            self._update_status(f"Trying {model}...", "indigo")
            try:
                prompt = AI_PROMPT.format(raw_text=raw_text)
                response = self.ai_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=80,
                    temperature=0.0
                )
                ai_answer = response.choices[0].message.content.strip()
                used_model = model
                break
            except Exception as e:
                ai_answer = f"Model {model} failed: {str(e)}"
        final_text = f"Used model: {used_model}\n\n{ai_answer}"
        self._finish(final_text)

    def _finish(self, text):
        self._stop_spinner()
        self._set_text(self.answer_text, text)
        color = "forestgreen" if "Cannot" not in text and "failed" not in text.lower() else "darkred"
        self._update_status("Done", color)
        self.copy_btn.state(["!disabled"] if text.strip() else ["disabled"])
        self.running = False
        self.btn.state(["!disabled"])

    def _finish_error(self, msg):
        self._stop_spinner()
        self._update_status(msg, "red")
        self._set_text(self.raw_text, msg)
        self.running = False
        self.btn.state(["!disabled"])

    def _clear_all(self):
        self._set_text(self.raw_text, "")
        self._set_text(self.answer_text, "")

    def _set_text(self, widget, text):
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", text.strip())
        widget.see("end")
        widget.configure(state="disabled")

    def _update_status(self, msg, color):
        def _upd():
            self.status_var.set(msg)
            self.status_label.configure(foreground=color)
        self.root.after(0, _upd)

    def _start_spinner(self):
        def spin():
            if not self.running: return
            c = self.spin_chars[self.spin_index % len(self.spin_chars)]
            self.spin_var.set(f"{c} processing")
            self.spin_index = (self.spin_index + 1) % len(self.spin_chars)
            self.root.after(130, spin)
        self.spin_index = 0
        spin()

    def _stop_spinner(self):
        self.spin_var.set("")

    def copy_answer(self):
        text = self.answer_text.get("1.0", tk.END).strip()
        if text:
            pyperclip.copy(text)
            messagebox.showinfo("Copied", "Copied Field")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizSolverApp(root)
    root.mainloop()
