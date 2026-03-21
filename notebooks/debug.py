from __future__ import annotations

import marimo as mo
from signalweaver.core.logging_config import configure_logging
from signalweaver.tasks.detect_language import detect_language
from signalweaver.tasks.extract_articles import extract_articles
from signalweaver.tasks.fetch_feed import fetch_feed
from signalweaver.tasks.group_by_language import group_by_language
from signalweaver.tasks.load_config import load_config
from signalweaver.tasks.select_feed import select_feed

configure_logging()

app = mo.App()


@app.cell
def _():
    config = load_config()
    return config


@app.cell
def _(config):
    feed_url = select_feed(config)
    return feed_url


@app.cell
def _(feed_url):
    feed = fetch_feed(feed_url)
    return extract_articles(feed)


@app.cell
def _(extract_articles):
    detected = [detect_language(a) for a in extract_articles]
    return group_by_language(detected)


if __name__ == '__main__':
    app.run()
