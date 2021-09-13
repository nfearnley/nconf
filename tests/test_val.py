from datetime import datetime, date, time, timezone
import toml
from nconf import config


def test_str():
    conf_text = """
    keyword = "value"
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        keyword: str

    conf = TestConf.load(conf_data)

    assert conf.keyword == "value"
    assert isinstance(conf.keyword, str)


def test_int():
    conf_text = """
    keyword = 1
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        keyword: int

    conf = TestConf.load(conf_data)

    assert conf.keyword == 1
    assert isinstance(conf.keyword, int)


def test_float():
    conf_text = """
    keyword = 1.5
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        keyword: float

    conf = TestConf.load(conf_data)

    assert conf.keyword == 1.5
    assert isinstance(conf.keyword, float)


def test_bool():
    conf_text = """
    keyword = true
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        keyword: float

    conf = TestConf.load(conf_data)

    assert conf.keyword is True
    assert isinstance(conf.keyword, bool)


def test_datetime():
    conf_text = """
    without_tz = 1985-02-08T12:34:56
    with_tz = 1985-02-08T12:34:56Z
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        without_tz: datetime
        with_tz: datetime

    conf = TestConf.load(conf_data)

    assert conf.without_tz == datetime(1985, 2, 8, 12, 34, 56)
    assert isinstance(conf.without_tz, datetime)
    assert conf.with_tz == datetime(1985, 2, 8, 12, 34, 56, tzinfo=timezone.utc)
    assert isinstance(conf.with_tz, datetime)


def test_date():
    conf_text = """
    keyword = 1985-02-08
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        keyword: date

    conf = TestConf.load(conf_data)

    assert conf.keyword == date(1985, 2, 8)
    assert isinstance(conf.keyword, date)


def test_time():
    conf_text = """
    keyword = 12:34:56
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        keyword: time

    conf = TestConf.load(conf_data)

    assert conf.keyword == time(12, 34, 56)
    assert isinstance(conf.keyword, time)
