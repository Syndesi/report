from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class NormalizedRssFeedDocument:
    title: str
    url: str
    description: str | None
    published: datetime | None
    source_language: str
    source_document: dict[str, Any]
