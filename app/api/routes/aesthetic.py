"""审美训练每日题 API。"""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.services.aesthetic_questions import (
    check_answer,
    get_daily_questions,
    get_stats_summary,
)

router = APIRouter(prefix="/aesthetic", tags=["aesthetic"])


class AnswerRequest(BaseModel):
    question_id: str = Field(..., description="题目 ID")
    choice: str = Field(..., description="用户选择 A 或 B")


@router.get("/daily")
async def daily_questions(
    date_str: str | None = Query(None, alias="date", description="日期 YYYY-MM-DD，默认今天"),
):
    """获取每日审美训练题目。"""
    target = date.fromisoformat(date_str) if date_str else date.today()
    questions = get_daily_questions(target)
    return {
        "date": target.isoformat(),
        "day_of_year": target.timetuple().tm_yday,
        "questions": questions,
        "total": len(questions),
    }


@router.post("/check")
async def check_answer_endpoint(body: AnswerRequest):
    """提交答案并获取解析。"""
    result = check_answer(body.question_id, body.choice)
    return result


@router.get("/stats")
async def stats():
    """题库统计信息。"""
    return get_stats_summary()
