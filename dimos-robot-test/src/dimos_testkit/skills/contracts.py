from __future__ import annotations

from pydantic import BaseModel, Field


class MoveSkillArgs(BaseModel):
    """Example typed args for a ``move``-like skill (align with DimOS @skill schema)."""

    x: float = Field(..., description="Forward velocity in m/s")
    duration: float = Field(default=2.0, ge=0.0, description="Duration in seconds")
