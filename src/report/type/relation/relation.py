from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RelationData(BaseModel):
    model_config = ConfigDict(extra='allow')


class Relation(BaseModel):
    id: UUID | None = None
    type: str
    start: UUID
    end: UUID
    data: RelationData
