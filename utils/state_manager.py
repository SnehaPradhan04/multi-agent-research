import json
import os
from typing import Dict, Optional, List
from datetime import datetime


class StateManager:
    
    def __init__(self, storage_path: str = "data/reports"):

        self.storage_path = storage_path
        
        os.makedirs(storage_path, exist_ok=True)
    
    def save_report(self, topic: str, report_data: Dict) -> str:
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_'))
        safe_topic = safe_topic.replace(' ', '_')[:50]  
        
        filename = f"report_{safe_topic}_{timestamp}.json"
        filepath = os.path.join(self.storage_path, filename)
        
        data = {
            'topic': topic,
            'timestamp': timestamp,
            'datetime': datetime.now().isoformat(),
            'report': report_data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_report(self, filename: str) -> Optional[Dict]:
        
        filepath = os.path.join(self.storage_path, filename)
        
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading report: {e}")
            return None
    
    def list_reports(self) -> List[str]:
        
        if not os.path.exists(self.storage_path):
            return []
        
        files = [
            f for f in os.listdir(self.storage_path) 
            if f.endswith('.json') and f.startswith('report_')
        ]
        
        files.sort(
            key=lambda x: os.path.getmtime(os.path.join(self.storage_path, x)),
            reverse=True
        )
        
        return files