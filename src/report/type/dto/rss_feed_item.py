from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class RssFeedItem:
    title: str
    url: str
    authors: list[str]
    tags: list[str]
    description: str | None
    published: datetime | None
    source_item: dict[str, Any]
