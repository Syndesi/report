import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import math
    import os
    from dataclasses import dataclass
    from datetime import datetime, timedelta, timezone

    import httpx
    import pandas as pd
    import plotly.express as px

    return dataclass, datetime, httpx, math, os, pd, px, timedelta, timezone


@app.cell
def _(os):
    api_key = os.environ['ANTHROPIC_ADMIN_API_KEY']
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
    starting_at = (datetime.now(timezone.utc) - timedelta(days=(2 * 7 + 1))).strftime('%Y-%m-%dT%H:%M:%SZ')

    response = httpx.get(
        'https://api.anthropic.com/v1/organizations/cost_report',
        headers={
            'anthropic-version': '2023-06-01',
            'X-Api-Key': api_key,
        },
        params={'starting_at': starting_at, 'limit': 31},
    )
    response.raise_for_status()
    raw = response.json()
    return (raw,)


@app.cell
def _(CostResult, datetime, math, pd):
    def parse_results(data: dict) -> list[CostResult]:
        results = []
        for bucket in data['data']:
            day = datetime.fromisoformat(bucket['starting_at'].replace('Z', '+00:00'))
            if bucket['results']:
                for r in bucket['results']:
                    results.append(
                        CostResult(
                            day=day,
                            currency=r['currency'],
                            amount=float(r['amount']),
                        )
                    )
            else:
                results.append(CostResult(day=day, currency='USD', amount=0.0))
        return results

    def to_dataframe(results: list[CostResult]) -> pd.DataFrame:
        df = pd.DataFrame([{'day': r.day.date(), 'cost_usd': r.amount} for r in results])
        df = df.groupby('day', as_index=False)['cost_usd'].sum().sort_values('day')
        df['cost_usd'] = df['cost_usd'].apply(lambda x: math.ceil(x) / 100)
        return df

    return parse_results, to_dataframe


@app.cell
def _(parse_results, pd, px, raw, to_dataframe):
    _results = parse_results(raw)
    _df = to_dataframe(_results)

    _ticks = []
    _labels = []
    for _day in _df['day']:
        _d = pd.Timestamp(_day)
        if _d.weekday() == 0:  # Monday
            _labels.append(f'{_d.strftime("%a")}<br>{_d.strftime("%d.%m.%Y")}')
        else:
            _labels.append(_d.strftime('%a'))
        _ticks.append(_day)

    _fig = px.bar(
        _df,
        x='day',
        y='cost_usd',
        labels={'day': 'Day', 'cost_usd': 'Cost (USD)'},
        title='Anthropic API Cost — Last 2 Weeks',
        template='plotly_white',
    )
    _fig.update_layout(
        yaxis_range=[0, max(2, _df['cost_usd'].max())],
        yaxis={
            'tickprefix': '$',
            'tickformat': '.2f',
        },
    )
    _fig.update_xaxes(
        tickvals=_ticks,
        ticktext=_labels,
        ticklabelmode='period',
    )
    _fig.update_traces(hovertemplate='<b>%{x|%a, %d.%m.%Y}</b><br>Cost: $%{y:.2f}<extra></extra>')
    _fig
    return


@app.cell
def _(parse_results, pd, px, raw, to_dataframe):
    _results = parse_results(raw)
    _df = to_dataframe(_results)
    _df = _df.sort_values('day').copy()
    _df['cumulative_cost_usd'] = _df['cost_usd'].cumsum()

    # Append today with same cumulative value as last data point
    _today = pd.Timestamp('today').normalize()
    if _today > pd.Timestamp(_df['day'].iloc[-1]):
        _df = pd.concat([
            _df,
            pd.DataFrame({'day': [_today], 'cost_usd': [0], 'cumulative_cost_usd': [_df['cumulative_cost_usd'].iloc[-1]]})
        ], ignore_index=True)

    _ticks = []
    _labels = []
    for _day in _df['day']:
        _d = pd.Timestamp(_day)
        if _d.weekday() == 0:  # Monday
            _labels.append(f'{_d.strftime("%a")}<br>{_d.strftime("%d.%m.%Y")}')
        else:
            _labels.append(_d.strftime('%a'))
        _ticks.append(_day)

    _fig = px.line(
        _df,
        x='day',
        y='cumulative_cost_usd',
        labels={'day': 'Day', 'cumulative_cost_usd': 'Cumulative Cost (USD)'},
        title='Anthropic API Cost — Last 2 Weeks (Cumulative)',
        template='plotly_white',
        line_shape='hv',
    )
    _fig.update_layout(
        yaxis={
            'tickprefix': '$',
            'tickformat': '.2f',
            'rangemode': 'tozero',
            'automargin': True,
        },
    )
    _fig.update_xaxes(
        tickvals=_ticks,
        ticktext=_labels,
        ticklabelmode='period',
    )
    _fig.update_traces(hovertemplate='<b>%{x|%a, %d.%m.%Y}</b><br>Cumulative Cost: $%{y:.2f}<extra></extra>')
    _fig
    return


if __name__ == "__main__":
    app.run()
