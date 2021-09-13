import toml
from nconf import config, section


def test_nconf():
    conf_text = """
    [bot]
    prefix = ";"
    name = "Beep boop"

    [discord]
    authtoken = "asdsadsadsadsadsadsadsadsa"
    logchannelid = 2342352332523
    admins = [123412351235, 23423432432]

    [api]
    cuttly = "asdasdsadasdsadsadsads"
    """

    conf_data = toml.loads(conf_text)

    @config
    class TestConf:
        @section
        class bot:
            prefix: str
            name: str
            height: int = 6

        @section
        class discord:
            authtoken: str
            logchannelid: int
            admins: list[int]

        @section
        class api:
            cuttly: str

    conf = TestConf.load(conf_data)
    assert conf.bot.prefix == ";"
    assert conf.bot.name == "Beep boop"
    assert conf.bot.height == 6
    assert conf.discord.authtoken == "asdsadsadsadsadsadsadsadsa"
    assert conf.discord.logchannelid == 2342352332523
    assert conf.discord.admins == [123412351235, 23423432432]
    assert conf.api.cuttly == "asdasdsadasdsadsadsads"
