from utils.llm_client import GroqClient
from utils.logger import AgentLogger


class FactCheckerAgent:
    
    def __init__(self, api_key: str, temperature: float = 0.3):
        self.client = GroqClient(api_key, temperature)
        self.logger = AgentLogger()
    
    async def verify(self, report: str, topic: str) -> str:
        """
        Verify the report quality
        
        Args:
            report: The report to check
            topic: Research topic
        """
        
        self.logger.log("Fact-Checker Agent", "Checking report...")
        
        if not report:
            return "No report to check."
        
        prompt = f"""Review this research report about: {topic}

Report:
{report}

Provide a quality assessment:

## Logical Consistency
- Is the report well-structured?
- Do arguments make sense?
- Any contradictions?

## Content Quality  
- Is information clear?
- Is it comprehensive?
- Are claims supported?

## Balance
- Multiple perspectives shown?
- Any obvious bias?

## Strengths
- What's done well?

## Areas for Improvement
- What could be better?

## Overall Assessment
Rate confidence level: HIGH / MEDIUM / LOW
Explain your rating."""

        try:
            verification = await self.client.complete(
                system_prompt="You are a quality checker. Review content carefully and fairly.",
                user_prompt=prompt,
                max_tokens=1000
            )
            
            self.logger.log("Fact-Checker Agent", "Verification done", "success")
            return verification
            
        except Exception as e:
            self.logger.log("Fact-Checker Agent", f"Error: {str(e)}", "error")
            raise Exception(f"Verification failed: {str(e)}")