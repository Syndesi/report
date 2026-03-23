from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

from .relation import Relation


class OwnsData(BaseModel):
    model_config = ConfigDict(extra='allow')


class Owns(Relation):
    type: Literal['OWNS']
    data: OwnsData
