from __future__ import annotations

import pytest
from pydantic import ValidationError

from rsssignalweaver.type.node import Node


def test_node_parsing_full_data():
    payload = {
        'id': '46fabacf-a487-45e5-8bab-df26087784d6',
        'type': 'Node',
        'data': {
            'name': 'name',
            'string': 'some string',
            'int': 1234,
            'float': 4.321,
            'boolean': True,
        },
    }

    node = Node.model_validate(payload)

    assert node.type == 'Node'
    assert str(node.id) == '46fabacf-a487-45e5-8bab-df26087784d6'
    assert node.data.name == 'name'
    assert node.data.string == 'some string'
    assert node.data.int == 1234
    assert node.data.float == 4.321
    assert node.data.boolean is True


def test_node_parsing_minimal_data():
    payload = {
        'type': 'Node',
        'data': {},
    }

    node = Node.model_validate(payload)

    assert node.type == 'Node'
    assert node.id is None
    # Minimal data should still allow access, just no attributes
    assert node.data.model_dump() == {}


def test_node_parsing_invalid_uuid():
    payload = {
        'id': 'not-a-uuid',
        'type': 'Node',
        'data': {},
    }

    with pytest.raises(ValidationError) as exc_info:
        Node.model_validate(payload)

    assert 'Input should be a valid UUID' in str(exc_info.value)
