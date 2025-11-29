from typing import List, Dict
from datetime import datetime


class AgentLogger:
    
    _logs: List[Dict] = []
    
    def log(self, agent: str, message: str, log_type: str = "info"):
        
        log_entry = {
            'agent': agent,
            'message': message,
            'type': log_type,
            'timestamp': datetime.now().isoformat()
        }
        
        self._logs.append(log_entry)
    
    def get_logs(self) -> List[Dict]:
        return self._logs.copy()
    
    def clear(self):
        self._logs.clear()