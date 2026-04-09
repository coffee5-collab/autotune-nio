import logging

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.models.schemas import AnalysisResult
from app.services.audio_analyzer import AudioAnalyzer
from app.services.eq_calculator import EQCalculator

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Audio Analysis"])

_analyzer = AudioAnalyzer()
_eq_calc = EQCalculator()

_ALLOWED_EXTENSIONS = (".wav", ".m4a", ".mp3", ".flac", ".aac", ".ogg", ".webm")


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_audio(file: UploadFile = File(...)):
    """
    Upload an in-cabin recording; receive frequency analysis + 7 EQ filters.

    Accepts WAV, M4A, MP3, FLAC, AAC, OGG.
    """
    filename = (file.filename or "").lower()
    if not filename.endswith(_ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail=f"不支持的音频格式。请使用：{', '.join(_ALLOWED_EXTENSIONS)}",
        )

    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="上传文件为空")

    try:
        measured, sample_rate, duration = _analyzer.analyze(contents)
    except Exception as e:
        logger.exception("Audio analysis failed")
        raise HTTPException(status_code=422, detail=f"音频解析失败：{e}")

    try:
        target, error, filters, score, summary = _eq_calc.calculate(measured)
    except Exception as e:
        logger.exception("EQ calculation failed")
        raise HTTPException(status_code=500, detail=f"EQ 计算失败：{e}")

    return AnalysisResult(
        measured_curve=measured,
        target_curve=target,
        error_curve=error,
        eq_filters=filters,
        overall_score=score,
        summary=summary,
        sample_rate=sample_rate,
        duration=round(duration, 2),
    )
