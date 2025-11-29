from typing import Dict, List
import asyncio
from duckduckgo_search import DDGS
from utils.llm_client import GroqClient
from utils.logger import AgentLogger


class ResearchAgent:
    
    def __init__(self, api_key: str, max_results: int = 5):
        self.client = GroqClient(api_key)
        self.max_results = max_results
        self.logger = AgentLogger()
    
    async def research(self, topic: str, depth: str = "standard") -> Dict:
        """
        Research a topic by searching the web
        
        Args:
            topic: What to research
            depth: "quick" (1 search), "standard" (2 searches), "deep" (3 searches)
        """
        
        self.logger.log("Research Agent", f"Researching: {topic}")
        
        num_searches = {
            "quick": 1,
            "standard": 2, 
            "deep": 3
        }.get(depth, 2)
        
        queries = await self._create_search_queries(topic, num_searches)
        self.logger.log("Research Agent", f"Created {len(queries)} search queries")
        
        all_results = []
        for query in queries:
            results = await self._search_web(query)
            all_results.extend(results)
        
        self.logger.log("Research Agent", f"Found {len(all_results)} sources", "success")
        
        summary = await self._summarize_findings(topic, all_results)
        
        return {
            'queries': queries,
            'results': all_results,
            'synthesis': summary
        }
    
    async def _create_search_queries(self, topic: str, num: int) -> List[str]:
        
        if num == 1:
            return [topic]
        
        prompt = f"""Create {num} different search queries for researching: {topic}

Make them diverse to cover different angles.
Keep each query short (3-8 words).
Return only the queries, one per line."""

        try:
            response = await self.client.complete(
                system_prompt="You create search queries.",
                user_prompt=prompt,
                max_tokens=150
            )
            
            queries = []
            for line in response.strip().split('\n'):
                line = line.strip()
                line = line.lstrip('0123456789.-) ')
                if line:
                    queries.append(line)
            
            return queries[:num]
            
        except:
            return [topic]
    
    async def _search_web(self, query: str) -> List[Dict]:
        """Search DuckDuckGo for the query"""
        
        self.logger.log("Research Agent", f"Searching: {query}")
        
        try:
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(None, self._ddgs_search, query)
            return results
            
        except Exception as e:
            self.logger.log("Research Agent", f"Search failed: {str(e)}", "warning")
            return []
    
    def _ddgs_search(self, query: str) -> List[Dict]:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=self.max_results))
                return results
        except:
            return []
    
    async def _summarize_findings(self, topic: str, results: List[Dict]) -> str:
        
        if not results:
            return f"No information found for: {topic}"
        
        results_text = ""
        for i, result in enumerate(results[:10], 1):  
            title = result.get('title', 'No title')
            body = result.get('body', 'No description')[:300]  
            results_text += f"\n**Source {i}:**\nTitle: {title}\nContent: {body}...\n"
        
        prompt = f"""Summarize research findings about: {topic}

{results_text}

Create a summary with:
1. Key findings
2. Important facts
3. Main themes"""

        try:
            summary = await self.client.complete(
                system_prompt="You summarize research clearly and concisely.",
                user_prompt=prompt,
                max_tokens=1000
            )
            return summary
            
        except:
            return f"Found {len(results)} sources about {topic}"