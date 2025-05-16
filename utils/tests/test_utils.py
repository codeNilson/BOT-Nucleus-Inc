from ..date_time_utils import parse_date_time

def test_parse_date_time_function():
    assert "25/05/2025T18:00:00Z" == parse_date_time("25/05/2025 15:00")