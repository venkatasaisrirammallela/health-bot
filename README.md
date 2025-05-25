# Health AI Chatbot

An intelligent health chatbot that combines voice interaction, AI-powered diagnosis, and expert medical advice using Google's Gemini model.

## Features

- 🤖 AI-powered health consultation using Google Gemini
- 🎤 Voice input and output capabilities
- 🔍 Symptom-based triage and dynamic questioning
- 🧠 ML-based preliminary diagnosis
- 🎯 Age verification and input validation
- 💬 Context-aware conversation handling

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file and add your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

Run the application:
```bash
python main.py
```

For GUI version:
```bash
streamlit run main.py
```

## Important Notes

- This chatbot is for preliminary screening only
- Always consult a licensed medical professional for proper diagnosis
- The AI model's responses should not be considered as medical advice
- Age verification is required (18+ only)

## Project Structure

- `main.py` - Application entry point
- `chatbot.py` - Core chatbot logic
- `voice_handler.py` - Voice input/output handling
- `ml_diagnosis.py` - ML model for diagnosis
- `utils.py` - Utility functions

## Dependencies

See `requirements.txt` for full list of dependencies.

## License

MIT License 