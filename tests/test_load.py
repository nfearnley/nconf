import pytest
import toml
from nconf import config


def test_class_load():
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


def test_instance_load():
    conf_text = """
    keyword = "value"
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        keyword: str

    conf = TestConf()
    conf.load(conf_data)

    assert conf.keyword == "value"
    assert isinstance(conf.keyword, str)


def test_rename_class_load():
    conf_text = """
    keyword = 1
    """

    conf_data = toml.loads(conf_text)

    @config(load="read")
    class TestConf:
        keyword: int

    conf = TestConf.read(conf_data)

    assert conf.keyword == 1
    assert isinstance(conf.keyword, int)


def test_rename_instance_load():
    conf_text = """
    keyword = "value"
    """

    conf_data = toml.loads(conf_text)

    @config(load="read")
    class TestConf:
        keyword: str

    conf = TestConf()
    conf.read(conf_data)

    assert conf.keyword == "value"
    assert isinstance(conf.keyword, str)


def test_rename_config():
    with pytest.raises(ValueError):
        @config(load="keyword")
        class TestConf:
            keyword: int
