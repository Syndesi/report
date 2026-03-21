from __future__ import annotations

import marimo

__generated_with = '0.20.4'
app = marimo.App(width='medium')


@app.cell
def _():
    import uuid

    import marimo as mo

    return mo, uuid


@app.cell
def _(mo):
    mo.output.append('hi :D')
    return


@app.cell
def _():
    import sys

    # sys.path.append("/app/src")
    sys.path
    return


@app.cell
def _():
    from rsssignalweaver.type.node import RssFeed

    data = {
        'name': 'name',
        'url': 'https://www.optimistdaily.com/feed/',
        'created': '2020-01-01T00:00:00+00:00',
        'updated': '2020-01-01T00:00:00+00:00',
    }

    feed = RssFeed(data=data)

    feed
    return (feed,)


@app.cell(hide_code=True)
def _(feed, mo):
    mo.md(f"""
    ### RssFeed as JSON

    ```json
    {feed.model_dump_json(indent=2)}
    ```
    """)
    return


@app.cell
def _(feed, uuid):
    feed.id = uuid.UUID('c18449c2-532d-47d6-91e9-463d3edd3e01')
    return


@app.cell(hide_code=True)
def _(feed, mo):
    mo.md(f"""
    ### RssFeed as JSON

    ```json
    {feed.model_dump_json(indent=2)}
    ```
    """)
    return


@app.cell
def _():
    import feedparser

    rss_feed = feedparser.parse('https://www.optimistdaily.com/feed/')
    return (rss_feed,)


@app.cell
def _(rss_feed):
    rss_feed
    return


@app.cell
def _(rss_feed):
    from rsssignalweaver.type.dto import RssFeedItem

    parsed_items = []
    for entry in rss_feed['entries']:
        title = entry['title']
        url = entry['link']
        authors = []
        for entry_author in entry['authors']:
            authors.append(entry_author['name'])
        tags = []
        for entry_tag in entry['tags']:
            tags.append(entry_tag['term'])
        description = entry['summary']
        published = entry['published_parsed']
        source_item = entry
        rss_feed_item = RssFeedItem(title, url, authors, tags, description, published, source_item)
        parsed_items.append(rss_feed_item)

    parsed_items[0]
    return (parsed_items,)


@app.cell
def _(mo, parsed_items):
    from dataclasses import asdict

    mo.json(asdict(parsed_items[5]))
    return


if __name__ == '__main__':
    app.run()
