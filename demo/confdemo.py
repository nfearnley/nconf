from pathlib import Path
import toml
from nconf import config, section


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


p = Path("testdata.conf")
conf = TestConf.load(toml.load(p))
print(conf)
