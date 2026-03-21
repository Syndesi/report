from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NodeData(BaseModel):
    model_config = ConfigDict(extra='allow')


class Node(BaseModel):
    id: UUID | None = None
    type: str
    data: NodeData
