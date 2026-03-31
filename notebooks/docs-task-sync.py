import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import requests
    import marimo as mo

    return mo, os, requests


@app.cell
def _(os):
    AUTH_DOMAIN = os.environ["AUTH_DOMAIN"]
    AUTH_USERNAME = os.environ["AUTH_USERNAME"]
    AUTH_PASSWORD = os.environ["AUTH_PASSWORD"]
    DOCS_DOMAIN = os.environ["DOCS_DOMAIN"]
    DOCS_API_KEY = os.environ["DOCS_API_KEY"]
    return AUTH_DOMAIN, AUTH_PASSWORD, AUTH_USERNAME, DOCS_API_KEY, DOCS_DOMAIN


@app.cell
def _(AUTH_DOMAIN, AUTH_PASSWORD, AUTH_USERNAME, requests):
    session = requests.Session()

    _resp = session.post(
        f"https://{AUTH_DOMAIN}/api/firstfactor",
        json={
            "username": AUTH_USERNAME,
            "password": AUTH_PASSWORD,
            "keepMeLoggedIn": False,
        },
    )
    _resp.raise_for_status()
    return (session,)


@app.cell
def _(DOCS_API_KEY, DOCS_DOMAIN, mo, session):
    def get_collection_id_by_name(response_data: dict, name: str) -> str:
        for item in response_data.get("data", []):
            if item.get("name") == name:
                return item["id"]
        raise ValueError(f"No collection found with name '{name}'")

    _resp = session.post(
        f"https://{DOCS_DOMAIN}/api/collections.list",
        headers={"Authorization": f"Bearer {DOCS_API_KEY}"},
        json={
          "offset": 0,
          "limit": 25,
          "sort": "updatedAt",
          "direction": "DESC"
        }
    )
    _resp.raise_for_status()
    _response_data = _resp.json()

    career_development_collection_id = get_collection_id_by_name(_response_data, "Career Development")
    mo.md(
        f'''
        ### Outline

        Career development collection id: `{career_development_collection_id}`
        '''
    )
    return


@app.cell
def _():
    return


@app.cell
def _(DOCS_API_KEY, DOCS_DOMAIN, session):
    _resp = session.post(
        f"https://{DOCS_DOMAIN}/api/documents.list",
        headers={"Authorization": f"Bearer {DOCS_API_KEY}"},
        json={
            "offset": 25,
            "limit": 25,
            "sort": "updatedAt",
            "direction": "DESC",
        },
    )
    _resp.raise_for_status()
    _docs = _resp.json()
    _docs
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
