import toml
from nconf import config, section


def test_section():
    conf_text = """
    [title]
    keyword = "value"
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        @section
        class title:
            keyword: str

    conf = TestConf.load(conf_data)

    assert conf.title.keyword == "value"
    assert isinstance(conf.title.keyword, str)


def test_external_section():
    conf_text = """
    [title]
    keyword = "value"
    """

    conf_data = toml.loads(conf_text)

    @section
    class Title:
        keyword: str

    @config
    class TestConf:
        title: Title

    conf = TestConf.load(conf_data)

    assert conf.title.keyword == "value"
    assert isinstance(conf.title.keyword, str)


def test_reused_section():
    conf_text = """
    [title1]
    keyword = "value1"
    [title2]
    keyword = "value2"
    """

    conf_data = toml.loads(conf_text)

    @section
    class Title:
        keyword: str

    @config
    class TestConf:
        title1: Title
        title2: Title

    conf = TestConf.load(conf_data)

    assert conf.title1.keyword == "value1"
    assert isinstance(conf.title1.keyword, str)
    assert conf.title2.keyword == "value2"
    assert isinstance(conf.title2.keyword, str)


def test_list_section():
    conf_text = """
    [[title]]
    keyword = "value1"
    [[title]]
    keyword = "value2"
    """

    conf_data = toml.loads(conf_text)

    @section
    class Title:
        keyword: str

    @config
    class TestConf:
        title: list[Title]

    conf = TestConf.load(conf_data)

    assert isinstance(conf.title, list)
    assert conf.title[0].keyword == "value1"
    assert isinstance(conf.title[0].keyword, str)
    assert conf.title[1].keyword == "value2"
    assert isinstance(conf.title[1].keyword, str)
