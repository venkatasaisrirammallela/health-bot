from flask import Flask, render_template, request, jsonify
from chatbot import HealthChatbot
import os

app = Flask(__name__)
chatbot = HealthChatbot(use_voice=True)  # Initialize with voice support

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Get response from chatbot
        response, followup = chatbot._handle_general_health_query(user_message)
        
        # Format the response to match frontend expectations
        messages = [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": response}
        ]
        
        return jsonify({
            'messages': messages,
            'followup_question': followup
        })
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")  # Add logging
        return jsonify({'error': str(e)}), 500

@app.route('/voice', methods=['POST'])
def handle_voice():
    try:
        # Handle voice input here
        # This will be implemented when voice functionality is needed
        return jsonify({'status': 'Voice endpoint ready'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Make sure GROQ_API_KEY is set
    if not os.getenv('GROQ_API_KEY'):
        raise ValueError("GROQ_API_KEY environment variable not set")
    
    # Run in production mode without debug
    app.run(host='127.0.0.1', port=5000, debug=False) 
