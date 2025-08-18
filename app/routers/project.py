from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import get_db
from ..models import Project, ChatSession
from ..schemas import ProjectCreateRequest, ProjectReply

router = APIRouter(prefix="/project", tags=["project"])

@router.post("/create", response_model=ProjectReply)
async def create_project(body: ProjectCreateRequest, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(ChatSession).where(ChatSession.id == body.session_id))
    cs = q.scalar_one_or_none()
    if cs is None:
        raise HTTPException(status_code=404, detail="Session not found")
    plan = {
        "steps": [
            "Соберём 10 наблюдений (сосчитай яблоки/игрушки)",
            "Сделаем таблицу: что и сколько получилось",
            "Соберём мини-презентацию (3 слайда) для родителей"
        ],
        "data_schema": {"item": "string", "count": "int"}
    }
    pr = Project(session_id=cs.id, title=body.title, plan=plan, data=None)
    db.add(pr)
    await db.commit()
    await db.refresh(pr)
    return ProjectReply(project_id=pr.id, title=pr.title, plan=pr.plan) 