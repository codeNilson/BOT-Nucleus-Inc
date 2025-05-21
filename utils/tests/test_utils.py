from datetime import datetime
from zoneinfo import ZoneInfo
import pytest
from ..date_time_utils import parse_date_time


def test_parse_date_time_returns_a_datetime_object():
    expected = datetime.strptime("25/05/2025 15:00", "%d/%m/%Y %H:%M")
    expected = expected.replace(tzinfo=ZoneInfo("America/Sao_Paulo"))
    assert expected == parse_date_time("25/05/2025 15:00")


def test_parse_date_time_raises_value_error_on_invalid_format():
    invalid_date_time = "2025-05-25 15:00"
    expected_message = "Formato inválido. Use o formato: DD/MM/AAAA HH:MM"
    with pytest.raises(ValueError) as exc_info:
        parse_date_time(invalid_date_time)
    assert str(exc_info.value) == expected_message
