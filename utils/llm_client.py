import aiohttp
import asyncio
import time


class GroqClient:
    
    def __init__(self, api_key: str, temperature: float = 0.7):
        self.api_key = api_key
        self.temperature = temperature
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"
        
        self.last_request_time = 0
        self.min_wait_time = 0.5 
    
    async def complete(self, system_prompt: str, user_prompt: str, 
                      max_tokens: int = 2000) -> str:
        
        for attempt in range(3):
            try:
                await self._wait_if_needed()
                
                response = await self._make_request(system_prompt, user_prompt, max_tokens)
                return response
                
            except Exception as e:
                if attempt == 2:  
                    raise Exception(f"API failed after 3 tries: {str(e)}")
                
                await asyncio.sleep((attempt + 1) * 2)
        
        raise Exception("API request failed")
    
    async def _wait_if_needed(self):
        time_passed = time.time() - self.last_request_time
        
        if time_passed < self.min_wait_time:
            wait_time = self.min_wait_time - time_passed
            await asyncio.sleep(wait_time)
        
        self.last_request_time = time.time()
    
    async def _make_request(self, system_prompt: str, user_prompt: str, max_tokens: int) -> str:
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": max_tokens
        }
        
        timeout = aiohttp.ClientTimeout(total=60)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(self.base_url, headers=headers, json=data) as response:
                
                if response.status != 200:
                    error = await response.text()
                    raise Exception(f"API Error {response.status}: {error}")
                
                result = await response.json()
                
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                else:
                    raise Exception("Invalid API response")