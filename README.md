# Gemini File Robot 🤖

A Python CLI tool that uses Google's Gemini AI to organize and manage your files using natural language commands.

## Features
- **Natural Language Control**: Ask the robot to "find all PDFs" or "list files on desktop".
- **Smart Actions**: Automatically identifies whether to list or collect files.
- **Quota Efficient**: Uses `gemini-2.5-flash` for high performance and reliability.

## Setup

1. **Clone the repository**
2. **Install Dependencies**:
   ```bash
   pip install google-generativeai python-dotenv
   ```
3. **Get an API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/) to get your Gemini API key.
   - Create a file named `APIKEY.env` in the root directory.
   - Add your key: `GEMINI_API_KEY=your_key_here`

## Usage

Run the robot:
```bash
python filebot.py
```

### Example Commands:
- "List all files on my Desktop"
- "Find all jpg images in my specific_folder and move them to a new folder"
