from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field


# ── Frequency Response ──────────────────────────────────────────────

class FrequencyPoint(BaseModel):
    frequency: float = Field(..., description="Center frequency in Hz")
    magnitude_db: float = Field(..., description="Magnitude in dB (ref=max)")


class FrequencyResponse(BaseModel):
    points: list[FrequencyPoint]
    sample_rate: int
    duration: float


# ── Parametric EQ Filter ────────────────────────────────────────────

class FilterType(str, Enum):
    BELL = "Bell"
    LOW_SHELF = "Low Shelf"
    HIGH_SHELF = "High Shelf"


class EQFilter(BaseModel):
    type: FilterType
    frequency: int = Field(..., ge=20, le=20000, description="Center frequency (Hz)")
    gain: float = Field(..., ge=-10.0, le=10.0, description="Gain in dB")
    q_factor: float = Field(..., ge=0.5, le=10.0, description="Q factor (bandwidth)")


# ── Analysis Result ─────────────────────────────────────────────────

class AnalysisResult(BaseModel):
    measured_curve: list[FrequencyPoint] = Field(
        ..., description="1/3-octave smoothed measured response"
    )
    target_curve: list[FrequencyPoint] = Field(
        ..., description="Harman-style automotive target curve"
    )
    error_curve: list[FrequencyPoint] = Field(
        ..., description="Target minus measured (compensation needed)"
    )
    eq_filters: list[EQFilter] = Field(
        ..., description="7 parametric EQ filters for NIO Pro EQ"
    )
    overall_score: float = Field(
        ..., description="Flatness score 0-100"
    )
    summary: str
    sample_rate: int
    duration: float
