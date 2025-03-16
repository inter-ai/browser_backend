# app/main.py

from fastapi import FastAPI, HTTPException
from app.knowledge_graph import KnowledgeGraphManager
from app.agent_manager import AgentManager
from app.tasks_manager import TaskManager
from app.models import AgentSearchRequest, DroneReport

app = FastAPI(title="Dual KG Demo", version="1.0")

kg_manager = KnowledgeGraphManager()
agent_manager = AgentManager()
task_manager = TaskManager()

@app.get("/")
def root():
    return {"message": "Dual Knowledge Graph API (Agent + Environment)"}

# -----------------------------------------------------------
# 1. Agent KG (Static)
# -----------------------------------------------------------

@app.get("/agent/kg/dump")
def dump_agent_kg():
    """
    Returns the entire Agent KG in Turtle.
    """
    turtle_data = kg_manager.dump_agent_kg()
    return {"graph": turtle_data}

@app.post("/agent/kg/search")
def search_agent_kg(req: AgentSearchRequest):
    """
    e.g. { "agent_name": "FireAgent" }
    Returns that agent’s snippet in Turtle.
    """
    if not req.agent_name:
        raise HTTPException(status_code=400, detail="Missing agent_name")
    turtle_data = kg_manager.search_agent_knowledge(req.agent_name)
    if not turtle_data:
        return {"message": f"Agent '{req.agent_name}' not found or no data."}
    return {"graph": turtle_data}

# Optionally, dynamic registration for new agents
@app.post("/agent/register")
def register_agent(name: str, agent_type: str):
    # e.g. pass capabilities as a list or just empty
    agent_id = agent_manager.register_agent(name, agent_type, capabilities=[])
    return {"agent_id": agent_id, "status": "registered"}

# -----------------------------------------------------------
# 2. Environment KG (Dynamic)
# -----------------------------------------------------------

@app.get("/environment/kg/dump")
def dump_environment_kg():
    """
    Returns the entire Environment KG in Turtle.
    """
    turtle_data = kg_manager.dump_environment_kg()
    return {"graph": turtle_data}

@app.post("/environment/drone_report")
def drone_report(report: DroneReport):
    """
    e.g. {
      "location": "RedwoodForest",
      "severity": "HighSeverity",
      "fireSpreadRate": 8.0,
      "airQuality": 200,
      "visibleFlames": 10
    }
    """
    kg_manager.update_environment_with_drone(report.dict())
    return {"message": "Environment updated with drone report", "data": report.dict()}

# -----------------------------------------------------------
# 3. Tasks (Optional)
# -----------------------------------------------------------

@app.post("/tasks")
def create_task(description: str, agent_id: str):
    t_id = task_manager.create_task(description, agent_id)
    return {"task_id": t_id, "status": "created"}

@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    t = task_manager.get_task(task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    return t
