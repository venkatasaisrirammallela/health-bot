// Voice input component for Streamlit
class VoiceInput {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.setupSpeechRecognition();
    }

    setupSpeechRecognition() {
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                // Send the transcript to Streamlit// Voice input component for Streamlit
class VoiceInput {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.setupSpeechRecognition();
    }

    setupSpeechRecognition() {
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                // Send the transcript to Streamlit
                window.parent.postMessage({
                    type: 'voiceInput',
                    data: transcript
                }, '*');
            };

            this.recognition.onend = () => {
                this.isListening = false;
                this.updateButtonState();
            };

            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.isListening = false;
                this.updateButtonState();
            };
        }
    }

    toggleListening() {
        if (!this.recognition) {
            console.error('Speech recognition not supported');
            return;
        }

        if (this.isListening) {
            this.recognition.stop();
        } else {
            this.recognition.start();
        }
        this.isListening = !this.isListening;
        this.updateButtonState();
    }

    updateButtonState() {
        const button = document.getElementById('voiceInputButton');
        if (button) {
            button.innerHTML = this.isListening ? 
                '<span style="color: red;">●</span> Listening...' : 
                '🎤 Click to Speak';
            button.style.backgroundColor = this.isListening ? '#ffebee' : '';
        }
    }
}

// Initialize voice input when the component is loaded
const voiceInput = new VoiceInput();

// Create and inject the voice input button
const button = document.createElement('button');
button.id = 'voiceInputButton';
button.innerHTML = '🎤 Click to Speak';
button.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 10px 20px;
    border-radius: 20px;
    border: none;
    background-color: #f0f2f6;
    cursor: pointer;
    font-size: 14px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    z-index: 1000;
    transition: all 0.3s ease;
`;

button.addEventListener('mouseover', () => {
    button.style.backgroundColor = '#e0e2e6';
});

button.addEventListener('mouseout', () => {
    if (!voiceInput.isListening) {
        button.style.backgroundColor = '#f0f2f6';
    }
});

button.addEventListener('click', () => {
    voiceInput.toggleListening();
});

document.body.appendChild(button);
                window.parent.postMessage({
                    type: 'voiceInput',
                    data: transcript
                }, '*');
            };

            this.recognition.onend = () => {
                this.isListening = false;
                this.updateButtonState();
            };

            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.isListening = false;
                this.updateButtonState();
            };
        }
    }

    toggleListening() {
        if (!this.recognition) {
            console.error('Speech recognition not supported');
            return;
        }

        if (this.isListening) {
            this.recognition.stop();
        } else {
            this.recognition.start();
        }
        this.isListening = !this.isListening;
        this.updateButtonState();
    }

    updateButtonState() {
        const button = document.getElementById('voiceInputButton');
        if (button) {
            button.innerHTML = this.isListening ? 
                '<span style="color: red;">●</span> Listening...' : 
                '🎤 Click to Speak';
            button.style.backgroundColor = this.isListening ? '#ffebee' : '';
        }
    }
}

// Initialize voice input when the component is loaded
const voiceInput = new VoiceInput();

// Create and inject the voice input button
const button = document.createElement('button');
button.id = 'voiceInputButton';
button.innerHTML = '🎤 Click to Speak';
button.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 10px 20px;
    border-radius: 20px;
    border: none;
    background-color: #f0f2f6;
    cursor: pointer;
    font-size: 14px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    z-index: 1000;
    transition: all 0.3s ease;
`;

button.addEventListener('mouseover', () => {
    button.style.backgroundColor = '#e0e2e6';
});

button.addEventListener('mouseout', () => {
    if (!voiceInput.isListening) {
        button.style.backgroundColor = '#f0f2f6';
    }
});

button.addEventListener('click', () => {
    voiceInput.toggleListening();
});

document.body.appendChild(button);
