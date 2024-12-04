import json
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from wsgiref.simple_server import make_server

SERVER_TIMEZONE = "UTC"


def get_current_time_in_zone(tz_name):
    try:
        tz = ZoneInfo(tz_name)
    except ZoneInfoNotFoundError:
        tz = ZoneInfo(SERVER_TIMEZONE)
    return datetime.now(tz)


def parse_datetime(data):
    try:
        dt = datetime.strptime(data["date"], "%m.%d.%Y %H:%M:%S")
    except ValueError:
        dt = datetime.strptime(data["date"], "%I:%M%p %Y-%m-%d")
    tz = ZoneInfo(data.get("tz", SERVER_TIMEZONE))
    return dt.replace(tzinfo=tz)


def application(environ, start_response):
    method = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]
    content_length = environ.get("CONTENT_LENGTH")
    body = environ["wsgi.input"].read(int(content_length)).decode("utf-8") if content_length else ""
    start_response("200 OK", [("Content-Type", "text/html")])

    # Route: GET /
    if method == "GET" and path == "/":
        current_time = get_current_time_in_zone(SERVER_TIMEZONE)
        return [f"<html><body>{current_time}</body></html>".encode()]

    # Route: GET /<tz_name>
    elif method == "GET" and path.startswith("/"):
        tz_name = path.lstrip("/")
        current_time = get_current_time_in_zone(tz_name)
        return [f"<html><body>{current_time}</body></html>".encode()]

    # Route: POST /api/v1/time
    elif method == "POST" and path == "/api/v1/time":
        data = json.loads(body) if body else {}
        tz = data.get("tz", SERVER_TIMEZONE)
        current_time = get_current_time_in_zone(tz)
        return [json.dumps({"time": current_time.isoformat()}).encode()]

    # Route: POST /api/v1/date
    elif method == "POST" and path == "/api/v1/date":
        data = json.loads(body) if body else {}
        tz = data.get("tz", SERVER_TIMEZONE)
        current_date = get_current_time_in_zone(tz).date()
        return [json.dumps({"date": current_date.isoformat()}).encode()]

    # Route: POST /api/v1/datediff
    elif method == "POST" and path == "/api/v1/datediff":
        data = json.loads(body)
        start = parse_datetime(data["start"])
        end = parse_datetime(data["end"])
        diff = (end - start).total_seconds()
        return [json.dumps({"difference_seconds": diff}).encode()]

    # 404 Not Found
    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"404 Not Found"]


if __name__ == "__main__":
    with make_server("", 8000, application) as server:
        print("Serving on port 8000...")
        server.serve_forever()
