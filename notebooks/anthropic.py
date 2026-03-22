import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import httpx
    import os
    from datetime import datetime, timezone, timedelta
    from dataclasses import dataclass
    import pandas as pd
    import plotly.express as px
    import math

    return dataclass, datetime, httpx, math, os, pd, px, timedelta, timezone


@app.cell
def _(os):
    api_key = os.environ["ANTHROPIC_ADMIN_API_KEY"]
    return (api_key,)


@app.cell
def _(dataclass, datetime):
    @dataclass
    class CostResult:
        day: datetime
        currency: str
        amount: float

    return (CostResult,)


@app.cell
def _(api_key, datetime, httpx, timedelta, timezone):
    starting_at = (datetime.now(timezone.utc) - timedelta(days=(2 * 7 + 1))).strftime("%Y-%m-%dT%H:%M:%SZ")

    response = httpx.get(
        "https://api.anthropic.com/v1/organizations/cost_report",
        headers={
            "anthropic-version": "2023-06-01",
            "X-Api-Key": api_key,
        },
        params={
            "starting_at": starting_at,
            "limit": 31
        },
    )
    response.raise_for_status()
    raw = response.json()
    return (raw,)


@app.cell
def _(CostResult, datetime, math, pd):
    def parse_results(data: dict) -> list[CostResult]:
        results = []
        for bucket in data["data"]:
            day = datetime.fromisoformat(bucket["starting_at"].replace("Z", "+00:00"))
            if bucket["results"]:
                for r in bucket["results"]:
                    results.append(CostResult(
                        day=day,
                        currency=r["currency"],
                        amount=float(r["amount"]),
                    ))
            else:
                results.append(CostResult(day=day, currency="USD", amount=0.0))
        return results


    def to_dataframe(results: list[CostResult]) -> pd.DataFrame:
        df = pd.DataFrame([{"day": r.day.date(), "cost_usd": r.amount} for r in results])
        df = df.groupby("day", as_index=False)["cost_usd"].sum().sort_values("day")
        df["cost_usd"] = df["cost_usd"].apply(lambda x: math.ceil(x) / 100)
        return df

    return parse_results, to_dataframe


@app.cell
def _(parse_results, pd, px, raw, to_dataframe):
    results = parse_results(raw)
    df = to_dataframe(results)

    ticks = []
    labels = []
    for day in df["day"]:
        d = pd.Timestamp(day)
        if d.weekday() == 0:  # Monday
            labels.append(f"{d.strftime('%a')}<br>{d.strftime('%d.%m.%Y')}")
        else:
            labels.append(d.strftime("%a"))
        ticks.append(day)

    fig = px.bar(
        df,
        x="day",
        y="cost_usd",
        labels={"day": "Day", "cost_usd": "Cost (USD)"},
        title="Anthropic API Cost — Last 2 Weeks",
        template="plotly_white"
    )
    fig.update_layout(
        yaxis_range=[0, max(5, df["cost_usd"].max())],
        yaxis={
            "tickprefix": "$",
            "tickformat": ".2f",
        },
    )
    fig.update_xaxes(
        tickvals=ticks,
        ticktext=labels,
        ticklabelmode="period",
    )
    fig.update_traces(
        hovertemplate="<b>%{x|%a, %d.%m.%Y}</b><br>Cost: $%{y:.2f}<extra></extra>"
    )
    fig
    return


if __name__ == "__main__":
    app.run()
