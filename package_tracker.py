#!/usr/bin/env python3
"""
Package Tracker with Todoist Integration - Enhanced Version
Automatically creates Todoist tasks when packages are delivered
Now includes due date functionality for better task tracking
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
    
    def create_task(self, content: str, description: str = None, 
                   project_id: str = None, due_string: str = None, 
                   priority: int = 1) -> Dict:
        """Create a new task in Todoist with enhanced options"""
        url = f"{self.base_url}/tasks"
        
        task_data = {
            "content": content,
            "priority": priority
        }
        
        if description:
            task_data["description"] = description
        if project_id:
            task_data["project_id"] = project_id
        if due_string:
            task_data["due_string"] = due_string
            
        response = requests.post(url, headers=self.headers, json=task_data)
        return response.json()

class PackageTracker:
    def __init__(self, todoist_token: str):
        self.todoist = TodoistIntegration(todoist_token)
        
    def calculate_due_date(self, package_type: str = "standard") -> str:
        """Calculate appropriate due date based on package type"""
        now = datetime.now()
        
        # Different due dates based on package urgency
        if package_type == "urgent":
            due_date = now + timedelta(hours=2)
            return "in 2 hours"
        elif package_type == "perishable":
            due_date = now + timedelta(hours=1)
            return "in 1 hour"
        elif package_type == "important":
            due_date = now + timedelta(hours=4)
            return "in 4 hours"
        else:  # standard
            due_date = now + timedelta(days=1)
            return "tomorrow"
    
    def determine_priority(self, package_type: str = "standard") -> int:
        """Determine task priority based on package type"""
        priority_map = {
            "urgent": 4,      # Highest priority
            "perishable": 4,  # Highest priority
            "important": 3,   # High priority
            "standard": 2     # Normal priority
        }
        return priority_map.get(package_type, 2)
        
    def handle_package_delivery(self, package_info: Dict) -> None:
        """Handle package delivery notification and create Todoist task with due date"""
        package_id = package_info.get('tracking_id', 'Unknown')
        sender = package_info.get('sender', 'Unknown Sender')
        delivery_time = package_info.get('delivery_time', datetime.now().isoformat())
        package_type = package_info.get('type', 'standard')  # New: package type
        
        # Calculate due date and priority
        due_string = self.calculate_due_date(package_type)
        priority = self.determine_priority(package_type)
        
        # Create task content
        task_content = f"📦 Package delivered: {package_id}"
        task_description = f"""
Package Details:
- Tracking ID: {package_id}
- Sender: {sender}
- Package Type: {package_type.title()}
- Delivered at: {delivery_time}
- Action needed: Check and process package contents

⏰ Due date set based on package urgency level.
Priority level: {priority}/4
        """.strip()
        
        # Create task in Todoist with due date
        try:
            task = self.todoist.create_task(
                content=task_content,
                description=task_description,
                due_string=due_string,
                priority=priority
            )
            print(f"✅ Task created successfully: {task.get('id', 'Unknown ID')}")
            print(f"📅 Due: {due_string}")
            print(f"⭐ Priority: {priority}/4")
            return task
        except Exception as e:
            print(f"❌ Error creating task: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    # Initialize tracker with Todoist API token
    tracker = PackageTracker("your_todoist_token_here")
    
    # Simulate different types of package deliveries
    test_packages = [
        {
            "tracking_id": "PKG123456789",
            "sender": "Amazon",
            "delivery_time": "2024-01-15T14:30:00Z",
            "type": "standard"
        },
        {
            "tracking_id": "URGENT987654321",
            "sender": "Medical Supply Co",
            "delivery_time": "2024-01-15T15:00:00Z",
            "type": "urgent"
        },
        {
            "tracking_id": "FOOD555666777",
            "sender": "Fresh Groceries",
            "delivery_time": "2024-01-15T15:30:00Z",
            "type": "perishable"
        }
    ]
    
    for package in test_packages:
        print(f"\n🚚 Processing delivery: {package['tracking_id']}")
        tracker.handle_package_delivery(package)