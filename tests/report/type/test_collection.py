from __future__ import annotations

from rsssignalweaver.type import Collection

payload = {
    'type': 'collection',
    'links': {
        'first': '/entities?page=1',
        'last': '/entities?page=3',
        'next': '/entities?page=2',
        'prev': None,
    },
    'items': [
        {
            'id': '8eaf7c74-7c88-4c91-a45d-5f8c3f2e1e21',
            'type': 'RssFeed',
            'data': {'name': 'Test', 'url': 'https://www.optimistdaily.com/feed/'},
        },
        {
            'id': '70fd8e4e-4f3e-4f60-bb7c-6bb06f4cbe55',
            'type': 'book',
            'data': {'title': '1984', 'pages': 328},
        },
        {
            'id': '91f98b2e-3c4b-4b3d-b3f3-7b5a42a89f11',
            'type': 'OWNS',
            'start': '8eaf7c74-7c88-4c91-a45d-5f8c3f2e1e21',
            'end': '70fd8e4e-4f3e-4f60-bb7c-6bb06f4cbe55',
            'data': {'since': 2021},
        },
    ],
}


def test_demo_parsing():
    collection = Collection.model_validate(payload)

    assert collection.type == 'collection'
