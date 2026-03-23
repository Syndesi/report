from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, HttpUrl

from .node import Node


class RssFeedData(BaseModel):
    name: str
    url: HttpUrl

    model_config = ConfigDict(extra='allow')


class RssFeed(Node):
    type: Literal['RssFeed'] = 'RssFeed'
    data: RssFeedData
