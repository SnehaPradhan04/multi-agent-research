from typing import Dict
from utils.llm_client import GroqClient
from utils.logger import AgentLogger


class WriterAgent:
    
    def __init__(self, api_key: str, temperature: float = 0.7):
        self.client = GroqClient(api_key, temperature)
        self.logger = AgentLogger()
    
    async def write_report(self, topic: str, research_data: Dict, analysis: str) -> str:
        
        self.logger.log("Writer Agent", "Writing report...")
        
        summary = research_data.get('synthesis', '')
        
        prompt = f"""Write a comprehensive research report about: {topic}

Research Findings:
{summary}

Analysis:
{analysis}

Create a professional report with these sections:

## Executive Summary
Brief overview of the report

## Introduction  
Background and context

## Key Findings
Main discoveries from research

## Analysis & Insights
Deep dive into what the findings mean

## Current Trends
What's happening now

## Challenges & Considerations
Important factors to consider

## Future Outlook
What to expect going forward

## Conclusions
Summary of main points

## Recommendations
Actionable suggestions

Use clear markdown formatting with proper headers."""

        try:
            report = await self.client.complete(
                system_prompt="You are a professional report writer. Write clear, well-structured reports.",
                user_prompt=prompt,
                max_tokens=2500
            )
            
            self.logger.log("Writer Agent", "Report written", "success")
            return report
            
        except Exception as e:
            self.logger.log("Writer Agent", f"Error: {str(e)}", "error")
            raise Exception(f"Writing failed: {str(e)}")