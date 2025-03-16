# app/agent_manager.py

import uuid

class AgentManager:
    def __init__(self):
        self.agents = {}

    def register_agent(self, name: str, agent_type: str, capabilities: list) -> str:
        agent_id = str(uuid.uuid4())
        self.agents[agent_id] = {
            "name": name,
            "type": agent_type,
            "capabilities": capabilities,
            "status": "idle",
            "current_task": None,
        }
        return agent_id

    def get_agent_status(self, agent_id: str):
        agent = self.agents.get(agent_id)
        return agent

    def assign_task(self, agent_id: str, task_description: str):
        if agent_id in self.agents:
            self.agents[agent_id]["status"] = "busy"
            self.agents[agent_id]["current_task"] = task_description
            return True
        return False
    
    def get_agent_info(self, agent_id: str):
        return self.agents.get(agent_id)
