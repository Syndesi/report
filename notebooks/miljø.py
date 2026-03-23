# /// script
# [tool.marimo.opengraph]
# title = "Miljø"
# description = "Environmental data"
# ///
from __future__ import annotations

import marimo

__generated_with = '0.21.1'
app = marimo.App(width='medium')


@app.cell
def _():
    import datetime
    import zoneinfo
    from dataclasses import dataclass
    from enum import StrEnum

    import marimo as mo
    import plotly.graph_objects as go
    from astral import LocationInfo
    from astral.sun import blue_hour, dawn, dusk, golden_hour, sun

    return (
        LocationInfo,
        StrEnum,
        blue_hour,
        dataclass,
        datetime,
        dawn,
        dusk,
        go,
        golden_hour,
        mo,
        sun,
        zoneinfo,
    )


@app.cell(hide_code=True)
def _(
    LocationInfo,
    StrEnum,
    blue_hour,
    dataclass,
    datetime,
    dawn,
    dusk,
    go,
    golden_hour,
    mo,
    sun,
    zoneinfo,
):
    class SolarColor(StrEnum):
        NIGHT = '#2f454d'
        ASTRONOMICAL_TWILIGHT = '#586a70'
        NAUTICAL_TWILIGHT = '#6f8f9a'
        CIVIL_TWILIGHT = '#96bbc9'
        DAY = '#b0dae8'
        MARKER = '#333333'

    @dataclass
    class SolarTimes:
        date: datetime.date
        timezone: zoneinfo.ZoneInfo
        astronomical_dawn: datetime.datetime
        nautical_dawn: datetime.datetime
        civil_dawn: datetime.datetime
        sunrise: datetime.datetime
        solar_noon: datetime.datetime
        sunset: datetime.datetime
        civil_dusk: datetime.datetime
        nautical_dusk: datetime.datetime
        astronomical_dusk: datetime.datetime
        golden_hour_morning: tuple[datetime.datetime, datetime.datetime]
        golden_hour_evening: tuple[datetime.datetime, datetime.datetime]
        blue_hour_morning: tuple[datetime.datetime, datetime.datetime]
        blue_hour_evening: tuple[datetime.datetime, datetime.datetime]

    def calculate_solar_times(
        lat: float,
        lon: float,
        tz: str,
        date: datetime.date | None = None,
    ) -> SolarTimes:
        if date is None:
            date = datetime.date.today()
        zone = zoneinfo.ZoneInfo(tz)
        loc = LocationInfo(latitude=lat, longitude=lon, timezone=tz)
        obs = loc.observer

        def _local(dt: datetime.datetime) -> datetime.datetime:
            return dt.astimezone(zone)

        s = sun(obs, date=date, tzinfo=zone)
        gh_morning = golden_hour(obs, date=date, direction=1, tzinfo=zone)
        gh_evening = golden_hour(obs, date=date, direction=2, tzinfo=zone)
        bh_morning = blue_hour(obs, date=date, direction=1, tzinfo=zone)
        bh_evening = blue_hour(obs, date=date, direction=2, tzinfo=zone)

        return SolarTimes(
            date=date,
            timezone=zone,
            astronomical_dawn=_local(dawn(obs, date=date, depression=18, tzinfo=zone)),
            nautical_dawn=_local(dawn(obs, date=date, depression=12, tzinfo=zone)),
            civil_dawn=_local(s['dawn']),
            sunrise=_local(s['sunrise']),
            solar_noon=_local(s['noon']),
            sunset=_local(s['sunset']),
            civil_dusk=_local(s['dusk']),
            nautical_dusk=_local(dusk(obs, date=date, depression=12, tzinfo=zone)),
            astronomical_dusk=_local(dusk(obs, date=date, depression=18, tzinfo=zone)),
            golden_hour_morning=(_local(gh_morning[0]), _local(gh_morning[1])),
            golden_hour_evening=(_local(gh_evening[0]), _local(gh_evening[1])),
            blue_hour_morning=(_local(bh_morning[0]), _local(bh_morning[1])),
            blue_hour_evening=(_local(bh_evening[0]), _local(bh_evening[1])),
        )

    def _to_hour_fraction(dt: datetime.datetime) -> float:
        return dt.hour + dt.minute / 60 + dt.second / 3600

    def _fmt_hm(dt: datetime.datetime) -> str:
        return dt.strftime('%H:%M')

    def _fmt(h: float) -> str:
        return f'{int(h):02d}:{int((h % 1) * 60):02d}'

    def create_solar_chart(solar: SolarTimes, title: str) -> go.Figure:
        ad = _to_hour_fraction(solar.astronomical_dawn)
        nd = _to_hour_fraction(solar.nautical_dawn)
        cd = _to_hour_fraction(solar.civil_dawn)
        sr = _to_hour_fraction(solar.sunrise)
        ss = _to_hour_fraction(solar.sunset)
        cdu = _to_hour_fraction(solar.civil_dusk)
        ndu = _to_hour_fraction(solar.nautical_dusk)
        adu = _to_hour_fraction(solar.astronomical_dusk)

        segments = [
            (0, ad, SolarColor.NIGHT, 'Astronomical night'),
            (ad, nd, SolarColor.ASTRONOMICAL_TWILIGHT, 'Astronomical twilight'),
            (nd, cd, SolarColor.NAUTICAL_TWILIGHT, 'Nautical twilight'),
            (cd, sr, SolarColor.CIVIL_TWILIGHT, 'Civil twilight'),
            (sr, ss, SolarColor.DAY, 'Daytime'),
            (ss, cdu, SolarColor.CIVIL_TWILIGHT, 'Civil twilight'),
            (cdu, ndu, SolarColor.NAUTICAL_TWILIGHT, 'Nautical twilight'),
            (ndu, adu, SolarColor.ASTRONOMICAL_TWILIGHT, 'Astronomical twilight'),
            (adu, 24, SolarColor.NIGHT, 'Astronomical night'),
        ]

        fig = go.Figure()
        seen = set()

        for start, end, color, label in segments:
            width = end - start
            if width <= 0:
                continue
            fig.add_trace(
                go.Bar(
                    x=[width],
                    y=[''],
                    base=start,
                    orientation='h',
                    marker_color=color,
                    name=label,
                    hovertemplate=(f'<b>{label}</b><br>{_fmt(start)} - {_fmt(end)}<extra></extra>'),
                    showlegend=label not in seen,
                )
            )
            seen.add(label)

        fig.update_layout(
            template='plotly_white',
            title={
                'text': f'{title} - {solar.date.strftime("%d.%m.%Y")} ({solar.timezone})',
                'font': {'size': 14},
            },
            barmode='stack',
            height=140,
            margin={'l': 10, 'r': 10, 't': 50, 'b': 40},
            xaxis={
                'range': [0, 24],
                'tickmode': 'array',
                'tickvals': list(range(0, 25, 2)),
                'ticktext': [f'{h:02d}:00' for h in range(0, 25, 2)],
                'tickfont': {'size': 11},
                'ticks': 'outside',
                'ticklen': 5,
                'tickwidth': 1,
                'tickcolor': '#555',
            },
            yaxis={'visible': False},
            bargap=0,
            showlegend=False,
        )

        return fig

    def create_solar_legend(solar: SolarTimes) -> mo.Html:
        tz = solar.timezone
        midnight_start = datetime.datetime(solar.date.year, solar.date.month, solar.date.day, tzinfo=tz)
        midnight_end = midnight_start + datetime.timedelta(days=1)

        # (color, name, [(start_dt | None, end_dt | None), ...])
        columns = [
            (
                SolarColor.NIGHT,
                'Night',
                [(None, solar.astronomical_dawn), (solar.astronomical_dusk, None)],
            ),
            (
                SolarColor.ASTRONOMICAL_TWILIGHT,
                'Astr. Twilight',
                [(solar.astronomical_dawn, solar.nautical_dawn), (solar.nautical_dusk, solar.astronomical_dusk)],
            ),
            (
                SolarColor.NAUTICAL_TWILIGHT,
                'Naut. Twilight',
                [(solar.nautical_dawn, solar.civil_dawn), (solar.civil_dusk, solar.nautical_dusk)],
            ),
            (
                SolarColor.CIVIL_TWILIGHT,
                'Civil Twilight',
                [(solar.civil_dawn, solar.sunrise), (solar.sunset, solar.civil_dusk)],
            ),
            (
                SolarColor.DAY,
                'Day',
                [(solar.sunrise, solar.sunset)],
            ),
        ]

        def _resolve(s, e):
            return (midnight_start if s is None else s, midnight_end if e is None else e)

        def _range_str(s, e) -> str:
            rs, re = _resolve(s, e)
            return f'{_fmt_hm(rs)} - {_fmt_hm(re)}'

        def _duration_str(intervals) -> str:
            secs = sum(int((_resolve(s, e)[1] - _resolve(s, e)[0]).total_seconds()) for s, e in intervals)
            h, rem = divmod(secs, 3600)
            return f'{h}h {rem // 60:02d}m'

        style = """
        <style>
          .solar-table {
            border-collapse: collapse;
            table-layout: fixed;
            width: 100%;
            font-family: sans-serif;
            font-size: 13px;
          }
          .solar-table th, .solar-table td {
            border: 1px solid #ddd;
            padding: 6px 8px;
            text-align: center;
            width: 20%;
            overflow: hidden;
            white-space: nowrap;
          }
          .solar-table th { background: #f5f5f5; font-weight: 600; }
          .solar-table td.total { font-weight: 600; }
          .swatch {
            display: inline-block;
            width: 12px; height: 12px;
            border-radius: 2px;
            margin-right: 5px;
            vertical-align: middle;
            border: 1px solid #ccc;
          }
        </style>
        """

        def _header(color, name):
            return f'<th><span class="swatch" style="background:{color};"></span>{name}</th>'

        def _row(cells, css_class):
            return ''.join(f'<td class="{css_class}">{c}</td>' for c in cells)

        headers = ''.join(_header(c, n) for c, n, _ in columns)
        row1 = _row([_range_str(*iv[0]) for *_, iv in columns], 'dim')
        row2 = _row(
            [_range_str(*iv[1]) if len(iv) >= 2 else '—' for *_, iv in columns],
            'dim',
        )
        row3 = _row([_duration_str(iv) for *_, iv in columns], 'total')

        html = f"""
        {style}
        <table class="solar-table">
          <thead><tr>{headers}</tr></thead>
          <tbody>
            <tr>{row1}</tr>
            <tr>{row2}</tr>
            <tr>{row3}</tr>
          </tbody>
        </table>
        """
        return mo.Html(html)

    return calculate_solar_times, create_solar_chart, create_solar_legend


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Chemnitz
    """)
    return


@app.cell
def _(calculate_solar_times, create_solar_chart, create_solar_legend, mo):
    chemnitz = calculate_solar_times(lat=50.827847, lon=12.921370, tz='Europe/Berlin')
    mo.output.append(mo.ui.plotly(create_solar_chart(chemnitz, 'Chemnitz')))
    mo.output.append(create_solar_legend(chemnitz))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Other places of interest
    """)
    return


@app.cell
def _(calculate_solar_times, create_solar_chart, mo):
    oslo = calculate_solar_times(lat=59.911491, lon=10.757933, tz='Europe/Berlin')
    mo.output.append(mo.ui.plotly(create_solar_chart(oslo, 'Oslo')))

    auckland = calculate_solar_times(lat=-36.848461, lon=174.763336, tz='Pacific/Auckland')
    mo.output.append(mo.ui.plotly(create_solar_chart(auckland, 'Auckland')))
    return


if __name__ == '__main__':
    app.run()
