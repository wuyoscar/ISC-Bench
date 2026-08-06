#!/usr/bin/env python3
"""Schema validation for eval samples."""
from __future__ import annotations

from pydantic import BaseModel, field_validator

MIN_WORDS = 40


class Sample(BaseModel):
    id: int
    prompt: str

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, v: str) -> str:
        if "???" in v:
            raise ValueError("prompt contains unresolved placeholder")
        if len(v.split()) < MIN_WORDS:
            raise ValueError(f"prompt length below minimum ({MIN_WORDS} words)")
        return v
