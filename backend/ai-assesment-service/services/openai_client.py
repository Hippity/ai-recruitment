import openai
import json
from typing import Dict, Any, Optional
from config import Config

class OpenAIClient:
    def __init__(self):
        if not Config.OPENAI_API_KEY:
            raise ValueError("OpenAI API key is required")
        
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
    
    def generate_completion(self, prompt: str, system_prompt: str = None) -> Dict[str, Any]:
        """
        Generate a completion from OpenAI with usage tracking
        """
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"}
            )
            
            # Extract response data
            content = response.choices[0].message.content
            usage = response.usage
            
            # Parse JSON response
            try:
                parsed_content = json.loads(content)
            except json.JSONDecodeError:
                parsed_content = {"error": "Invalid JSON response", "raw_content": content}
            
            return {
                "success": True,
                "content": parsed_content,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens
                },
                "model": self.model
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": None,
                "usage": None
            }