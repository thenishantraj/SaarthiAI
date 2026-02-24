import google.generativeai as genai
import streamlit as st
import re
from datetime import datetime
import database as db

class SocraticMentor:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.conversation_history = []
        self.doubt_score = 0
        self.hint_count = 0
        self.step_count = 0
        
    def detect_language(self, text):
        """Detect if text is Hindi, English, or Hinglish"""
        hindi_pattern = re.compile(r'[\u0900-\u097F]')
        if hindi_pattern.search(text):
            return "hinglish" if any(c.isascii() for c in text) else "hindi"
        return "english"
    
    def get_system_prompt(self, language):
        """Get the system prompt with language instruction"""
        base_prompt = """You are a Socratic Mentor. Never give direct answers. If a student asks a question, provide a hint or a leading question to help them think. Only provide the final answer after 3-4 successful steps of thinking.

Key Rules:
1. First response should always be a guiding question
2. Count the student's thinking steps
3. After 3-4 exchanges, you may reveal the answer
4. If the student seems stuck, provide a small hint
5. Always encourage independent thinking

Language: Respond in the same language the student uses."""
        
        return base_prompt
    
    def analyze_confidence(self, message):
        """Analyze user message for confidence/doubt indicators"""
        doubt_indicators = [
            "?", "help", "confused", "don't understand", "stuck",
            "hint", "explain", "how", "what", "why", "????",
            "samajh", "nahi aaya", "kya", "kaise", "pls", "please"
        ]
        
        confidence_indicators = [
            "got it", "understood", "understood", "yes", "okay",
            "acha", "thik hai", "samajh gaya", "pata hai"
        ]
        
        message_lower = message.lower()
        
        # Calculate doubt score
        doubt_count = sum(1 for word in doubt_indicators if word in message_lower)
        confidence_count = sum(1 for word in confidence_indicators if word in message_lower)
        
        score_change = (doubt_count * 5) - (confidence_count * 3)
        return max(-10, min(10, score_change))
    
    def extract_topic(self, message):
        """Extract main topic from message"""
        # Simple topic extraction (can be enhanced with NLP)
        common_topics = [
            "math", "science", "physics", "chemistry", "biology",
            "history", "geography", "english", "coding", "programming",
            "algebra", "calculus", "geometry", "trigonometry"
        ]
        
        message_lower = message.lower()
        for topic in common_topics:
            if topic in message_lower:
                return topic
        return "general"
    
    def get_response(self, user_message, user_id):
        """Get AI response with Socratic method"""
        
        # Detect language
        language = self.detect_language(user_message)
        
        # Analyze confidence
        confidence_change = self.analyze_confidence(user_message)
        self.doubt_score = max(0, min(100, self.doubt_score + confidence_change))
        
        # Extract topic
        topic = self.extract_topic(user_message)
        
        # Update progress
        db.update_user_progress(user_id, topic, -confidence_change if confidence_change < 0 else 2)
        
        # Build conversation context
        system_prompt = self.get_system_prompt(language)
        
        # Count hints requested
        if "hint" in user_message.lower() or "help" in user_message.lower():
            self.hint_count += 1
            self.doubt_score += 5
        
        # Prepare the full prompt
        full_prompt = f"""{system_prompt}

Current step count: {self.step_count}
Hints given so far: {self.hint_count}
Doubt score: {self.doubt_score}

User: {user_message}

Remember: {'This is step ' + str(self.step_count + 1) + ' of the thinking process' if self.step_count < 4 else 'You can now provide the full answer if appropriate'}

Your response:"""
        
        # Get response from Gemini
        response = self.model.generate_content(full_prompt)
        ai_response = response.text
        
        # Update step count
        self.step_count += 1
        if self.step_count >= 4:
            self.step_count = 0  # Reset for next topic
        
        # Save to database
        db.save_chat_message(user_id, "user", user_message, topic)
        db.save_chat_message(user_id, "assistant", ai_response, topic)
        
        return ai_response, self.doubt_score, topic

def get_rubric_feedback(text, text_type="essay"):
    """Get structured feedback using rubric"""
    
    rubric_prompts = {
        "essay": """
        Analyze this essay and provide feedback based on:
        1. Clarity (0-10): How clear and understandable is the writing?
        2. Logic (0-10): How logical is the argument/flow?
        3. Depth (0-10): How deep and insightful is the content?
        4. Structure (0-10): How well-organized is the essay?
        5. Grammar (0-10): How correct is the grammar and spelling?
        
        Provide specific suggestions for improvement.
        """,
        
        "code": """
        Analyze this code and provide feedback based on:
        1. Correctness (0-10): Does the code work correctly?
        2. Efficiency (0-10): How efficient is the solution?
        3. Readability (0-10): How readable and well-commented is it?
        4. Best Practices (0-10): Does it follow coding standards?
        5. Logic (0-10): How sound is the algorithmic logic?
        
        Provide specific suggestions for improvement.
        """
    }
    
    prompt = f"""{rubric_prompts[text_type]}

Text to analyze:
{text}

Provide feedback in this format:
## Overall Score: [Average]
### Category Scores:
- Clarity: [Score] - [Brief comment]
- Logic: [Score] - [Brief comment]
- Depth: [Score] - [Brief comment]
- Structure: [Score] - [Brief comment]
- Grammar: [Score] - [Brief comment]

### Strengths:
- [Point 1]
- [Point 2]

### Areas for Improvement:
- [Suggestion 1]
- [Suggestion 2]

### Specific Recommendations:
[Detailed advice for improvement]
"""
    
    return prompt
