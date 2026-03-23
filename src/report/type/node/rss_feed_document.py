from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_serializer

from .node import Node


class RssFeedDocumentData(BaseModel):
    retrieved: datetime | None = None

    model_config = ConfigDict(extra='allow')

    @field_serializer('retrieved', when_used='json')
    def serialize_dt(self, dt: datetime | None):
        if dt is None:
            return None
        return dt.isoformat()


class RssFeedDocument(Node):
    type: Literal['RssFeedDocument'] = 'RssFeedDocument'
    data: RssFeedDocumentData
