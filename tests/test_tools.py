
from tools import get_weather, get_country_info


def test_weather_tool_has_description():
    assert get_weather.name == "get_weather"
    assert get_weather.description


def test_country_tool_has_description():
    assert get_country_info.name == "get_country_info"
    assert get_country_info.description
