import datetime as dt

import httpx
import pytest
import respx
import time_machine
from dateutil.tz import tzoffset
from rich.table import Table

from netlify_builds.cli import (
    BuildRow,
    main,
    make_request,
    parse_response,
    print_table,
    read_config,
)


@pytest.fixture
async def async_client():
    async with httpx.AsyncClient() as client:
        yield client


@pytest.fixture
def mocked_config(mocker):
    read_text = mocker.patch("pathlib.Path.read_text")
    read_text.return_value = """{"my-team": "very-secret-token"}"""


@pytest.mark.usefixtures("mocked_config")
def test_read_config():
    config = read_config()

    assert config == {"my-team": "very-secret-token"}


@pytest.mark.asyncio
@respx.mock
async def test_make_request_success(async_client):
    respx.get("https://api.netlify.com/api/v1/my-team/builds/status").respond(
        json={"some-key": "some-value"}
    )

    team, content = await make_request(async_client, "my-team", "the-token")

    assert team == "my-team"
    assert content == {"some-key": "some-value"}


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code", [400, 403, 404, 500])
@respx.mock
async def test_make_request_error(async_client, status_code):
    respx.get("https://api.netlify.com/api/v1/my-team/builds/status").respond(
        status_code
    )

    team, content = await make_request(async_client, "my-team", "the-token")

    assert team == "my-team"
    assert content is None


@pytest.fixture
def dummy_response_data():
    return {
        "active": 0,
        "pending_concurrency": 0,
        "enqueued": 0,
        "minutes": {
            "current": 49,
            "current_average_sec": 158,
            "previous": 104,
            "period_start_date": "2019-10-15T00:00:00.000-07:00",
            "period_end_date": "2019-11-15T00:00:00.000-07:00",
            "last_updated_at": "2019-11-01T13:30:00.000-07:00",
            "included_minutes": 300,
            "included_minutes_with_packs": 300,
        },
        "build_count": 19,
    }


@time_machine.travel("2019-11-01 10:00")
def test_parse_response(dummy_response_data):
    build_row = parse_response("example", dummy_response_data)

    assert build_row.team == "example"
    assert build_row.used == 49
    assert build_row.total == 300
    assert build_row.start_date == dt.datetime(
        2019, 10, 15, 0, 0, tzinfo=tzoffset(None, -25200)
    )
    assert build_row.end_date == dt.datetime(
        2019, 11, 15, 0, 0, tzinfo=tzoffset(None, -25200)
    )
    assert int(build_row.percent_elapsed) == 55


@pytest.fixture
def console_print(mocker):
    yield mocker.patch("rich.console.Console.print")


def test_print_table_no_rows(console_print):
    print_table([])

    console_print.assert_called_once_with("No rows to print", style="bold red")


def test_print_table_with_rows(console_print):
    print_table(
        [
            BuildRow(
                team="a-team",
                used=30,
                total=300,
                start_date=dt.datetime(2019, 10, 15),
                end_date=dt.datetime(2019, 11, 15),
            ),
            BuildRow(
                team="blue",
                used=299,
                total=300,
                start_date=dt.datetime(2019, 10, 3),
                end_date=dt.datetime(2019, 11, 3),
            ),
        ]
    )

    console_print.assert_called_once()
    (arg_1,) = console_print.call_args[0]
    assert isinstance(arg_1, Table)


@pytest.mark.usefixtures("mocked_config")
@respx.mock
def test_e2e(dummy_response_data, console_print):
    respx.get("https://api.netlify.com/api/v1/my-team/builds/status").respond(
        json=dummy_response_data
    )
    main()

    console_print.assert_called_once()
    (arg_1,) = console_print.call_args[0]
    assert isinstance(arg_1, Table)
