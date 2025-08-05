#!/usr/bin/env python3
"""
Package Tracker with Todoist Integration
Automatically creates Todoist tasks when packages are delivered
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Optional

class TodoistIntegration:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.todoist.com/rest/v2"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def create_task(self, content: str, description: str = None, project_id: str = None) -> Dict:
        """Create a new task in Todoist"""
        url = f"{self.base_url}/tasks"
        
        task_data = {
            "content": content,
        }
        
        if description:
            task_data["description"] = description
        if project_id:
            task_data["project_id"] = project_id
            
        response = requests.post(url, headers=self.headers, json=task_data)
        return response.json()

class PackageTracker:
    def __init__(self, todoist_token: str):
        self.todoist = TodoistIntegration(todoist_token)
        
    def handle_package_delivery(self, package_info: Dict) -> None:
        """Handle package delivery notification and create Todoist task"""
        package_id = package_info.get('tracking_id', 'Unknown')
        sender = package_info.get('sender', 'Unknown Sender')
        delivery_time = package_info.get('delivery_time', datetime.now().isoformat())
        
        # Create task content
        task_content = f"Package delivered: {package_id}"
        task_description = f"""
Package Details:
- Tracking ID: {package_id}
- Sender: {sender}
- Delivered at: {delivery_time}
- Action needed: Check and process package contents
        """.strip()
        
        # Create task in Todoist
        try:
            task = self.todoist.create_task(
                content=task_content,
                description=task_description
            )
            print(f"Task created successfully: {task.get('id', 'Unknown ID')}")
            return task
        except Exception as e:
            print(f"Error creating task: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    # Initialize tracker with Todoist API token
    tracker = PackageTracker("your_todoist_token_here")
    
    # Simulate package delivery
    package_info = {
        "tracking_id": "PKG123456789",
        "sender": "Amazon",
        "delivery_time": "2024-01-15T14:30:00Z"
    }
    
    tracker.handle_package_delivery(package_info)