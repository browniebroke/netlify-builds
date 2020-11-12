import datetime as dt

from dateutil.tz import tzoffset

from netlify_builds.cli import parse_response


def test_parse_response():
    response_data = {
        "active": 0,
        "pending_concurrency": 0,
        "enqueued": 0,
        "minutes": {
            "current": 49,
            "current_average_sec": 158,
            "previous": 104,
            "period_start_date": "2019-10-15T00:00:00.000-07:00",
            "period_end_date": "2019-11-15T00:00:00.000-07:00",
            "last_updated_at": "2019-11-01T13:30:00.823Z",
            "included_minutes": 300,
            "included_minutes_with_packs": 300,
        },
        "build_count": 19,
    }

    parsed_response = parse_response("example", response_data)

    assert parsed_response[:-1] == (
        "example",
        49,
        dt.datetime(2019, 10, 15, 0, 0, tzinfo=tzoffset(None, -25200)),
        dt.datetime(2019, 11, 15, 0, 0, tzinfo=tzoffset(None, -25200)),
    )
    assert int(parsed_response[-1]) == 1270
