from typing import Dict
from utils.llm_client import GroqClient
from utils.logger import AgentLogger

class AnalysisAgent:
    def __init__(self, api_key: str, temperature: float=0.7):
        self.client = GroqClient(api_key, temperature)
        self.logger = AgentLogger()

    async def analyze(self, research_data: Dict, topic: str) -> str:
        self.logger.log("Analysis Agent", "Analyzing research data...")

        summary = research_data.get('synthesis', '')

        if not summary:
            return "Not enough to analyze."
        
        prompt = f"""Analyze this research about: {topic}

Research Summary:
{summary}

Provide analysis with:

1. **Main Themes**: What are the key themes?
2. **Key Insights**: What are the important discoveries?
3. **Patterns**: What patterns do you see?
4. **Implications**: What does this mean?
5. **Future Outlook**: Where is this heading?

Be thorough and insightful."""
        
        try:
            analysis = await self.client.complete(
                system_prompt="You are an expert analyst. Find deep insights and patterns.",
                user_prompt=prompt,
                max_tokens=1500
            )
        
            self.logger.log("Analysis Agent", "Analysis complete", "success")
            return analysis

        except Exception as e:
            self.logger.log("Analysis Agent", f"Error: {str(e)}", "error")
            raise Exception("Analysis failed: {str(e)}")