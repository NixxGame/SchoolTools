# Quiz Solver

A clean desktop tool that captures your screen, extracts quiz questions/options using local OCR, and automatically finds the correct answer using free AI models via OpenRouter.

Supports both classic multiple-choice questions and sort/drag-and-drop style questions.

## Features

- One-click screenshot capture
- Fully local OCR ( EasyOCR )
- AI answer generation with automatic model fallback
- Modern, professional UI with real-time status and copy button
- Handles messy OCR output intelligently

## Requirements

- **Python 3.9 or higher** (any version from 3.9 to the latest is fine)  
  Download from the official website:
  ```
  https://www.python.org/downloads/
  ```
  - Choose the latest stable release or any 3.9+ version  
  - **Windows**: Check the box "Add Python to PATH" during installation  
  - **macOS/Linux**: Usually pre-installed or install via package manager (brew, apt, etc.)

After installing, open `Command Prompt` / `Terminal` and verify:

```bash
python --version
```

You should see something like `Python 3.12.3` (or 3.9+).

## Installation

1. **Navigate to the project folder** in Command Prompt / Terminal  
   - Press `Win + R` and type `cmd` then press Enter
   - Use the `cd` command to change directory. Example:

     ```bash
     cd C:\Users\Name\Downloads\SchoolTools-main\SchoolTools-main
     ```

     (Replace with your actual folder path or copy it from File Explorer address bar)

2. **Install dependencies**  
   Run this single command inside the project folder:

     ```bash
     pip install -r requirements.txt
     ```

3. **Add your OpenRouter API key**  
   - Go to:
   ```https://openrouter.ai/keys```
   - Create a new key (any name works)  
   - Copy the key (starts with `sk-or-v1-`)  
   - Open `API-Key.txt` in the project folder  
   - Paste **only** the key (one line, no quotes, no extra text) then save

4. **Run the application**  
   In the same `Command Prompt` / `Terminal`, **make sure you're in the project folder** then run:

     ```bash
     python OCRQuizBot.py
     ```

## Usage

1. Open your quiz (e.g. Everfi)
2. Click `Capture & Solve`
3. Wait 5–30 seconds
4. See the AI's answer in the `Answer Field` box
5. Click `Copy Answer` to paste it or select the correct answer

## Troubleshooting

- Missing API key popup → add your OpenRouter key
- 404 model error → change model in `models.txt` and include the models to use (see `https://openrouter.ai/models?max_price=0`)
- 429 rate limit → wait a few minutes
- Bad OCR → ensure text is large/sharp on screen

## License

MIT – free to modify and share.










