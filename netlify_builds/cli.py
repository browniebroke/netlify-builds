import asyncio
import datetime as dt
import json
from pathlib import Path

import httpx
from dateutil.parser import parse
from httpx import HTTPError
from rich.console import Console
from rich.table import Table

console = Console()


def main():
    asyncio.run(run_async())


async def run_async():
    team_tokens = read_config()
    async with httpx.AsyncClient(timeout=3) as client:
        tasks = [
            make_request(client, team, token) for team, token in team_tokens.items()
        ]
        team_responses = await asyncio.gather(*tasks)
        rows = [
            parse_response(team, response_data)
            for team, response_data in team_responses
            if response_data
        ]
        print_table(rows)


def read_config():
    config_file = Path.home() / ".netlify-builds.json"
    return json.loads(config_file.read_text())


async def make_request(client, team, token):
    try:
        response = await client.get(
            f"https://api.netlify.com/api/v1/{team}/builds/status",
            headers={"content-length": "0", "authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
    except HTTPError:
        return team, None
    return team, response.json()


def parse_response(team, response_data):
    minutes = response_data["minutes"]
    start_date = parse(minutes["period_start_date"])
    end_date = parse(minutes["period_end_date"])
    used = minutes["current"]
    percent_elapsed = (
        100
        * (dt.datetime.now(tz=start_date.tzinfo) - start_date)
        / (end_date - start_date)
    )
    return team, used, start_date, end_date, percent_elapsed


def print_table(rows):
    if not rows:
        console.print("No rows to print", style="bold red")
        return

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Team", style="bold yellow")
    table.add_column("Mins", style="dim", justify="right")
    table.add_column("Start Date", style="dim")
    table.add_column("End Date", style="dim")
    table.add_column("Elapsed", justify="right")
    table.add_column("Used", justify="right")

    for team, used, start_date, end_date, percent_elapsed in rows:
        percent_used = 100 * used / 300
        style = "red" if percent_used > percent_elapsed else "green"
        table.add_row(
            team,
            f"{used} mins",
            f"{start_date:%Y-%m-%d}",
            f"{end_date:%Y-%m-%d}",
            f"[{style}]{percent_elapsed:.1f}%[/{style}]",
            f"[{style}]{percent_used:.1f}%[/{style}]",
        )

    console.print(table)
