from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(prefix="/eq", tags=["EQ Config"])


@router.get("/bands")
async def get_eq_config():
    """Return NIO Pro EQ configuration."""
    return {
        "num_filters": settings.EQ_FILTER_COUNT,
        "gain_range": {"min": settings.EQ_GAIN_MIN, "max": settings.EQ_GAIN_MAX},
        "q_range": {"min": settings.EQ_Q_MIN, "max": settings.EQ_Q_MAX},
        "filter_types": ["Bell", "Low Shelf", "High Shelf"],
    }
