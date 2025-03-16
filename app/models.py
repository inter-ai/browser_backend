# app/models.py

from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class WildfireEvent(BaseModel):
    event_id: str
    location: str
    severity: str  # e.g. "HighSeverity", "ModerateSeverity", "LowSeverity"

class UserCommand(BaseModel):
    """User command text for emergency scenarios."""
    user_command: str

class CommandStatus(BaseModel):
    command_id: str
    status: str
    details: Optional[str] = None



class AgentSearchRequest(BaseModel):
    agent_name: str

class DroneReport(BaseModel):
    location: str
    severity: str
    fireSpreadRate: float
    airQuality: int
    visibleFlames: float

class DKGUpdate(BaseModel):
    source: str
    subject: str
    predicate: str
    object: str

class DKGQueryRequest(BaseModel):
    query: str  # SPARQL or some simplified query

class AgentRegistration(BaseModel):
    agent_name: str
    agent_type: str
    capabilities: List[str]

class AgentAssignment(BaseModel):
    command_id: str
    task_description: str

class DecisionRequest(BaseModel):
    context: Dict[str, Any]
    goals: List[str]

class DecisionResponse(BaseModel):
    decision_id: str
    actions: List[str]
    reasoning: Optional[str] = None

class TaskCreateRequest(BaseModel):
    command_id: str
    task_description: str

class TaskStatus(BaseModel):
    task_id: str
    status: str
    progress: Optional[str] = None
