from __future__ import annotations

from pydantic import BaseModel, field_validator

from .element import Element
from .node import Node, RssFeed
from .relation import Owns, Relation

NODE_TYPES = {'RssFeed': RssFeed}

RELATION_TYPES = {
    'OWNS': Owns,
}


class CollectionLinks(BaseModel):
    first: str | None = None
    last: str | None = None
    next: str | None = None
    prev: str | None = None


class Collection(BaseModel):
    type: str
    links: CollectionLinks
    items: list[Element]

    @field_validator('items', mode='before')
    @classmethod
    def parse_items(cls, v):
        parsed = []

        for item in v:
            if 'start' in item and 'end' in item:
                model = RELATION_TYPES.get(item.get('type'), Relation)
            else:
                model = NODE_TYPES.get(item.get('type'), Node)

            parsed.append(model.model_validate(item))

        return parsed
