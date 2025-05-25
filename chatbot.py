import os
from typing import Dict, Optional, Tuple, List
from utils import (
    get_api_key, validate_age, validate_temperature,
    validate_yes_no, format_symptom_summary, clean_text
)
from groq import Groq

class HealthChatbot:
    def __init__(self, use_voice: bool = False):
        """Initialize the health chatbot."""
        self.use_voice = use_voice
        self.age = None
        self.conversation_history = []
        self.current_context = None
        self.last_question = None
        self.followup_count = 0
        self.followup_responses = []  # Store responses for summary
        
        # Initialize Groq API
        try:
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                raise ValueError("GROQ_API_KEY environment variable not set")
            
            self.client = Groq(api_key=api_key)
            print("Successfully initialized Groq client")
            
            # Keep the original system prompt
            self.system_prompt = """
            You are a health information assistant that:
            1. Provides clear, informative responses to health questions
            2. Asks relevant follow-up questions based on your responses
            3. Adapts to new questions when the user changes the topic
            4. Always recommends consulting healthcare professionals for medical advice
            
            When asking follow-up questions:
            - Make them specific and relevant to the current discussion
            - Focus on understanding the user's condition better
            - Ask one question at a time
            - Wait for the user's response before asking another question
            
            When responding to user answers:
            - Acknowledge their response
            - Provide relevant information
            - Ask the next logical follow-up question if needed
            
            Remember to:
            - Be clear and informative
            - Be cautious with medical advice
            - Encourage professional medical consultation
            """
            
            # Initialize chat history with system prompt
            self.chat_history = [{"role": "system", "content": self.system_prompt}]
            print("Chatbot initialized successfully")
            
        except Exception as e:
            print(f"Error initializing chatbot: {str(e)}")
            raise ValueError(f"Failed to initialize chatbot: {str(e)}")
    
    def _get_model_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from Groq model."""
        try:
            completion = self.client.chat.completions.create(
                model="llama3-70b-8192",  # Using Meta's Llama 3 model which is available on Groq
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                top_p=0.8,
                stream=False
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error getting model response: {str(e)}")
            raise
    
    def _get_followup_question(self, response: str) -> Optional[str]:
        """Generate a follow-up question based on the bot's response."""
        if self.followup_count >= 3:
            return None
            
        try:
            messages = self.chat_history + [
                {"role": "assistant", "content": response},
                {"role": "user", "content": "Based on my previous response, generate a single, relevant follow-up question that will help understand my condition better. The question should be directly related to the information just provided, specific, focused, easy to answer, and helpful for understanding my situation. Return only the question, nothing else."}
            ]
            
            question = self._get_model_response(messages).strip()
            question = question.strip('"\'')
            
            if question.endswith('?'):
                self.followup_count += 1
                return question
            return None
            
        except Exception as e:
            print(f"Error generating follow-up question: {str(e)}")
            return None
    
    def _generate_conclusion(self) -> str:
        """Generate a conclusion based on all follow-up responses."""
        try:
            messages = self.chat_history + [
                {"role": "user", "content": f"""
                Based on the following information:
                Initial query: {self.current_context}
                Follow-up responses: {self.conversation_history}
                
                Please provide a comprehensive conclusion that includes:
                1. Summary of the gathered information
                2. Clear recommendations
                3. When to seek medical attention
                4. Any important warnings or precautions
                5. Next steps
                
                Keep the conclusion clear and informative, but not too long.
                """}
            ]
            
            conclusion = self._get_model_response(messages)
            formatted_conclusion = f"""
            **Conclusion:**
            {conclusion}
            """
            
            return formatted_conclusion
            
        except Exception as e:
            print(f"Error generating conclusion: {str(e)}")
            return "I apologize, but I encountered an error while generating the conclusion."
    
    def _generate_summary(self) -> str:
        """Generate a summary based on the three follow-up responses."""
        try:
            messages = self.chat_history + [
                {"role": "user", "content": f"""
                Based on the following conversation:
                Initial query: {self.current_context}
                Follow-up responses: {self.followup_responses}
                
                Please provide a brief summary that includes:
                1. Key points from the user's responses
                2. Important observations
                3. General recommendations
                
                Important: Do not include any questions in your summary. Keep the summary concise and clear.
                """}
            ]
            
            summary = self._get_model_response(messages)
            # Remove any lines that end with question marks
            summary_lines = [line for line in summary.split('\n') if not line.strip().endswith('?')]
            summary_text = '\n'.join(summary_lines)
            
            formatted_summary = f"""
            **Summary of Our Discussion:**
            {summary_text}
            """
            
            return formatted_summary
            
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return "I apologize, but I encountered an error while generating the summary."
    
    def _handle_user_response(self, question: str, response: str) -> Tuple[str, Optional[str]]:
        """Handle the user's response to a follow-up question."""
        try:
            # Store the response for summary
            self.followup_responses.append({"question": question, "answer": response})
            
            # If this was the third question, generate a summary
            if self.followup_count >= 3:
                summary = self._generate_summary()
                # Reset for next conversation
                self.followup_count = 0
                self.followup_responses = []
                self.current_context = None
                self.last_question = None
                return summary, None
            
            messages = self.chat_history + [
                {"role": "user", "content": f"""
                Previous question: {question}
                User's response: {response}
                Current context: {self.current_context}
                
                Please provide:
                1. Acknowledgment of the user's response
                2. Relevant information based on their answer
                3. Clear explanation of what this means
                4. When to seek medical attention (if applicable)
                
                Important: Do not include any questions in your response. Keep the response clear and informative, but not too long.
                """}
            ]
            
            model_response = self._get_model_response(messages)
            # Remove any lines that end with question marks
            response_lines = [line for line in model_response.split('\n') if not line.strip().endswith('?')]
            response_text = '\n'.join(response_lines)
            
            # Update chat history
            self.chat_history.append({"role": "user", "content": response})
            self.chat_history.append({"role": "assistant", "content": response_text})
            
            # Generate the next follow-up question if we haven't reached the limit
            next_question = self._get_followup_question(response_text)
            
            return response_text, next_question
            
        except Exception as e:
            error_response = "I apologize, but I encountered an error while processing your response. Please try rephrasing your answer."
            print(f"Error in response handling: {str(e)}")
            return error_response, None
    
    def _handle_general_health_query(self, query: str) -> Tuple[str, Optional[str]]:
        """Handle general health queries and generate follow-up questions."""
        try:
            # Reset follow-up tracking for new conversation
            self.followup_count = 0
            self.followup_responses = []
            self.current_context = query
            self.last_question = None
            
            messages = self.chat_history + [
                {"role": "user", "content": f"""
                User query: {query}
                Current context: {self.current_context}
                
                Please provide:
                1. Clear information about the described symptoms or condition
                2. When to seek medical attention
                3. General wellness advice
                4. Recommended next steps
                
                Important: Do not include any questions in your response. Keep the response clear and informative, but not too long.
                """}
            ]
            
            model_response = self._get_model_response(messages)
            # Remove any lines that end with question marks
            response_lines = [line for line in model_response.split('\n') if not line.strip().endswith('?')]
            response_text = '\n'.join(response_lines)
            
            # Update chat history
            self.chat_history.append({"role": "user", "content": query})
            self.chat_history.append({"role": "assistant", "content": response_text})
            
            # Generate a follow-up question
            next_question = self._get_followup_question(response_text)
            self.last_question = next_question
            
            return response_text, next_question
            
        except Exception as e:
            error_response = "I apologize, but I encountered an error while processing your query. Please try rephrasing your question."
            print(f"Error in health query handling: {str(e)}")
            return error_response, None
    
    def cleanup(self) -> None:
        """Clean up resources."""
        try:
            self.conversation_history = []
            self.current_context = None
            self.last_question = None
            self.followup_count = 0
            self.followup_responses = []
            self.chat_history = [{"role": "system", "content": self.system_prompt}]
        except Exception as e:
            print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    chatbot = HealthChatbot()
    chatbot.run() 