from typing import Any

from pydantic import BaseModel, Field


class Source(BaseModel):
    name: str
    url: str


class Entity(BaseModel):
    id: str
    entity_type: str
    name: str
    description: str = ""
    url: str = ""
    categories: list[str] = Field(default_factory=list)
    source: Source
    metadata: dict[str, Any] = Field(default_factory=dict)