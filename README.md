markdown
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
  - Windows: Check "Add Python to PATH" during installation
  - macOS/Linux: Usually comes with Python or install via package manager

- Windows, macOS, or Linux operating system

After installing Python, verify it works by opening Command Prompt / Terminal and typing:

```bash
python --version
```

## Installation

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
   

2. Get a free OpenRouter API key:
   - Go to https://openrouter.ai/keys
   - Create a key (name it anything)
   - Copy the key (starts with `sk-or-v1-`)

3. Open `API-Key.` and paste your key exactly as shown:

   ```python
     sk-or-v1-********
   ```

4. Run:

   ```bash
   cd {project Path after extraction}
   python OCRQuizBot.py
   ```

## Usage

1. Open your quiz (e.g. Everfi)
2. **Zoom in tightly** so **only the question + options** (or sort items) are visible
   - F11 for full screen
   - Ctrl + mouse wheel to zoom
   - Hide tabs, bookmarks bar, sidebar
3. Click **Capture & Solve**
4. Wait 5–30 seconds
5. See the AI's answer
6. Click **Copy Answer** to paste it

## Tips for Best Results

- **Clean capture is key** – exclude browser UI, taskbar, icons
- If OCR is messy → increase screen contrast or zoom more
- Rate limit (429) → script auto-tries next model
- Sort questions → AI usually groups correctly (Saving / Investing)

## Troubleshooting

- Missing API key popup → add your OpenRouter key
- 404 model error → change model in `models.txt` and include the models to use (see https://openrouter.ai/models?max_price=0)
- 429 rate limit → wait a few minutes
- Bad OCR → ensure text is large/sharp on screen

## License

MIT – free to modify and share.

```







