# app/tasks_manager.py

import uuid

class TaskManager:
    def __init__(self):
        self.tasks = {}

    def create_task(self, description: str, agent_id: str):
        task_id = str(uuid.uuid4())
        self.tasks[task_id] = {
            "description": description,
            "agent_id": agent_id,
            "status": "created"
        }
        return task_id

    def update_task_status(self, task_id: str, status: str):
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = status

    def get_task(self, task_id: str):
        return self.tasks.get(task_id)
