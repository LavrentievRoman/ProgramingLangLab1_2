import requests

BASE_URL = "http://localhost:8000"


def test_root():
    response = requests.get(BASE_URL + "/")
    assert response.status_code == 200


def test_timezone():
    response = requests.get(BASE_URL + "/Europe/Moscow")
    assert response.status_code == 200


def test_time_api():
    response = requests.post(BASE_URL + "/api/v1/time", json={"tz": "Europe/Moscow"})
    assert response.status_code == 200
    assert "time" in response.json()


def test_date_api():
    response = requests.post(BASE_URL + "/api/v1/date", json={"tz": "Asia/Tokyo"})
    assert response.status_code == 200
    assert "date" in response.json()


def test_datediff_api():
    payload = {
        "start": {"date": "12.20.2021 22:21:05", "tz": "EST"},
        "end": {"date": "12:30pm 2020-12-01", "tz": "Europe/Moscow"}
    }
    response = requests.post(BASE_URL + "/api/v1/datediff", json=payload)
    assert response.status_code == 200
    assert "difference_seconds" in response.json()


if __name__ == "__main__":
    test_root()
    test_timezone()
    test_time_api()
    test_date_api()
    test_datediff_api()
    print("All tests passed!")
