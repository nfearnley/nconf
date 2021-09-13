from datetime import datetime, date, time, timezone
import toml
from nconf import config


def test_list_str():
    conf_text = """
    keyword = ["value1", "value2", "value3"]
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        keyword: list[str]

    conf = TestConf.load(conf_data)

    assert conf.keyword == ["value1", "value2", "value3"]
    assert isinstance(conf.keyword, list)
    assert all(isinstance(v, str) for v in conf.keyword)


def test_list_int():
    conf_text = """
    keyword = [1, 2, 3]
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        keyword: list[int]

    conf = TestConf.load(conf_data)

    assert conf.keyword == [1, 2, 3]
    assert isinstance(conf.keyword, list)
    assert all(isinstance(v, int) for v in conf.keyword)


def test_list_float():
    conf_text = """
    keyword = [1.5, 2.5, 3.5]
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        keyword: list[float]

    conf = TestConf.load(conf_data)

    assert conf.keyword == [1.5, 2.5, 3.5]
    assert isinstance(conf.keyword, list)
    assert all(isinstance(v, float) for v in conf.keyword)


def test_list_bool():
    conf_text = """
    keyword = [true, false, true]
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        keyword: list[bool]

    conf = TestConf.load(conf_data)

    assert conf.keyword == [True, False, True]
    assert isinstance(conf.keyword, list)
    assert all(isinstance(v, bool) for v in conf.keyword)


def test_list_datetime():
    conf_text = """
    without_tz = [1985-02-08T12:34:56, 1985-03-08T12:34:56, 1985-04-08T12:34:56]
    with_tz = [1985-02-08T12:34:56Z, 1985-03-08T12:34:56Z, 1985-04-08T12:34:56Z]
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        without_tz: list[datetime]
        with_tz: list[datetime]

    conf = TestConf.load(conf_data)

    assert conf.without_tz == [datetime(1985, 2, 8, 12, 34, 56), datetime(1985, 3, 8, 12, 34, 56), datetime(1985, 4, 8, 12, 34, 56)]
    assert isinstance(conf.without_tz, list)
    assert all(isinstance(v, datetime) for v in conf.without_tz)
    assert conf.with_tz == [datetime(1985, 2, 8, 12, 34, 56, tzinfo=timezone.utc), datetime(1985, 3, 8, 12, 34, 56, tzinfo=timezone.utc), datetime(1985, 4, 8, 12, 34, 56, tzinfo=timezone.utc)]
    assert isinstance(conf.with_tz, list)
    assert all(isinstance(v, datetime) for v in conf.with_tz)


def test_list_date():
    conf_text = """
    keyword = [1985-02-08, 1985-03-08, 1985-04-08]
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        keyword: list[date]

    conf = TestConf.load(conf_data)

    assert conf.keyword == [date(1985, 2, 8), date(1985, 3, 8), date(1985, 4, 8)]
    assert isinstance(conf.keyword, list)
    assert all(isinstance(v, date) for v in conf.keyword)


def test_list_time():
    conf_text = """
    keyword = [12:34:56, 12:34:57, 12:34:58]
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        keyword: list[time]

    conf = TestConf.load(conf_data)

    assert conf.keyword == [time(12, 34, 56), time(12, 34, 57), time(12, 34, 58)]
    assert isinstance(conf.keyword, list)
    assert all(isinstance(v, time) for v in conf.keyword)


def test_list_list_int():
    conf_text = """
    keyword = [[1,2,3], [4,5,6], [7,8,9]]
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        keyword: list[list[int]]

    conf = TestConf.load(conf_data)

    assert conf.keyword == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert isinstance(conf.keyword, list)
    assert all(isinstance(sublist, list) for sublist in conf.keyword)
    assert all(isinstance(v, int) for sublist in conf.keyword for v in sublist)
