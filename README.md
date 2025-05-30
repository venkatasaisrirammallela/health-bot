# Health AI Chatbot

An intelligent health chatbot that combines voice interaction, AI-powered diagnosis, and expert medical advice using Google's Gemini model.

## Features

- 🤖 AI-powered health consultation using Google Gemini
- 🎤 Voice input and output capabilities
- 🔍 Symptom-based triage and dynamic questioning
- 🎯 Age verification and input validation
- 💬 Context-aware conversation handling
- Save the conversation in csv and json fromat

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

- `app.py` - Application entry point
- `chatbot.py` - Core chatbot logic
- `voice_input.js` - Voice input/output handling
- `utils.py` - Utility functions

## Dependencies

See `requirements.txt` for full list of dependencies.

## License

MIT License 
