from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Any

Role = Literal["user", "ayya", "ayana", "system"]

class MessageIn(BaseModel):
    role: Role
    content: str

class TurnRequest(BaseModel):
    session_id: Optional[int] = None
    user_uid: str
    topic: Optional[str] = None
    messages: List[MessageIn] = Field(default_factory=list)

class TurnReply(BaseModel):
    role: Literal["ayya", "ayana", "system"]
    say: str
    animations: List[str] = Field(default_factory=list)
    next_task: Optional[str] = None

class CreateSessionRequest(BaseModel):
    user_uid: str
    topic: Optional[str] = None

class CreateSessionReply(BaseModel):
    session_id: int

class ProjectCreateRequest(BaseModel):
    session_id: int
    title: str

class ProjectReply(BaseModel):
    project_id: int
    title: str
    plan: dict 