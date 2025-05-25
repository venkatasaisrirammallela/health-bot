import pyttsx3
import speech_recognition as sr
from typing import Optional, Tuple
import time
import sys
import pyaudio

class VoiceHandler:
    def __init__(self):
        print("Initializing voice handler...")
        try:
            # Test PyAudio
            p = pyaudio.PyAudio()
            input_devices = []
            for i in range(p.get_device_count()):
                device_info = p.get_device_info_by_index(i)
                if device_info.get('maxInputChannels') > 0:  # Only input devices
                    input_devices.append(device_info)
            p.terminate()
            
            if not input_devices:
                raise Exception("No microphone found! Please connect a microphone.")
            print(f"Found {len(input_devices)} input devices:")
            for device in input_devices:
                print(f"- {device['name']}")
            
            # Initialize text-to-speech engine
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to set a female voice if available
                for voice in voices:
                    if "female" in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
            self.engine.setProperty('rate', 150)  # Speed of speech
            print("Text-to-speech engine initialized successfully")
            
            # Initialize speech recognizer
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 3000  # Lower threshold for better sensitivity
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8  # Shorter pause threshold
            
            # Test microphone
            print("Testing microphone...")
            with sr.Microphone() as source:
                print("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print("Microphone initialized successfully")
                
        except Exception as e:
            print(f"Error initializing voice handler: {str(e)}")
            print("\nTroubleshooting steps:")
            print("1. Check if a microphone is connected")
            print("2. Check if the microphone is set as default input device")
            print("3. Check if the microphone is not being used by another application")
            print("4. Try restarting the application")
            print("5. Check Windows sound settings")
            raise
        
    def speak(self, text: str) -> None:
        """Convert text to speech."""
        try:
            print(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
            print("Falling back to text output only")
            
    def listen(self, timeout: int = 5) -> Tuple[bool, Optional[str]]:
        """
        Listen for voice input and convert to text.
        Returns (success, text or None)
        """
        print("\n=== Starting Voice Input ===")
        print("Listening for voice input...")
        try:
            with sr.Microphone() as source:
                print("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                print("Ready to listen... (Speak now)")
                print("Waiting for speech...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
                print("Processing speech...")
                text = self.recognizer.recognize_google(audio)
                print(f"Successfully recognized: {text}")
                return True, text
                
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period")
            return False, None
        except sr.UnknownValueError:
            print("Could not understand audio - please speak clearly")
            return False, None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            print("Please check your internet connection")
            return False, None
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return False, None
    
    def interactive_voice_input(self, prompt: str, max_attempts: int = 3) -> Optional[str]:
        """
        Interactive voice input with retry logic.
        Returns the recognized text or None if all attempts fail.
        """
        print("\n=== Voice Input Mode ===")
        self.speak(prompt)
        
        for attempt in range(max_attempts):
            print(f"\nAttempt {attempt + 1} of {max_attempts}")
            print("Please speak your question...")
            success, text = self.listen()
            if success and text:
                return text
            
            if attempt < max_attempts - 1:
                retry_msg = "I didn't catch that. Could you please repeat?"
                print(retry_msg)
                self.speak(retry_msg)
                time.sleep(1)
        
        fallback_msg = "I'm having trouble understanding. Please type your response instead."
        print(fallback_msg)
        self.speak(fallback_msg)
        return None
    
    def cleanup(self) -> None:
        """Clean up resources."""
        try:
            print("Cleaning up voice handler resources...")
            self.engine.stop()
            print("Voice handler cleanup completed")
        except Exception as e:
            print(f"Error during cleanup: {e}")
            
    def speak(self, text: str) -> None:
        """Convert text to speech."""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
            
    def listen(self, timeout: int = 5) -> Tuple[bool, Optional[str]]:
        """
        Listen for voice input and convert to text.
        Returns (success, text or None)
        """
        with sr.Microphone() as source:
            print("Listening...")
            try:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio input
                audio = self.recognizer.listen(source, timeout=timeout)
                
                # Convert speech to text
                text = self.recognizer.recognize_google(audio)
                print(f"Recognized: {text}")
                return True, text
                
            except sr.WaitTimeoutError:
                print("No speech detected within timeout period")
                return False, None
            except sr.UnknownValueError:
                print("Could not understand audio")
                return False, None
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return False, None
            except Exception as e:
                print(f"Error in speech recognition: {e}")
                return False, None
    
    def interactive_voice_input(self, prompt: str, max_attempts: int = 3) -> Optional[str]:
        """
        Interactive voice input with retry logic.
        Returns the recognized text or None if all attempts fail.
        """
        self.speak(prompt)
        
        for attempt in range(max_attempts):
            success, text = self.listen()
            if success and text:
                return text
            
            if attempt < max_attempts - 1:
                self.speak("I didn't catch that. Could you please repeat?")
                time.sleep(1)
        
        self.speak("I'm having trouble understanding. Please type your response instead.")
        return None
    
    def cleanup(self) -> None:
        """Clean up resources."""
        try:
            self.engine.stop()
        except:
            pass 