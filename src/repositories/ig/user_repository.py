"""repositories.user_repository"""
#########################################################
# Builtin packages
#########################################################
import requests
from dataclasses import dataclass, field

#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
from common.log import debug
from common.config import Config
from repositories.ig import IgBaseRepository

CONFIG = Config().config


@dataclass
class UserRepository(IgBaseRepository):
    """user repository"""
    IG_USER_ID: str = field(init=False, default=CONFIG["IG"]["USER_ID"])
    FIELDS: str = field(init=False, default="biography,id,followers_count,media_count,username,website")

    def get(self) -> dict:
        """get user info through ig api

        Returns:
            dict: user info
        """
        url = (f"{self.BASE_URL}/{self.API_VERSION}/{self.IG_USER_ID}?"
               f"fields={self.FIELDS}&access_token={self.ACCESS_TOKEN}")
        debug("request user info to {0}", url)

        res = requests.get(url, timeout=30)
        debug("responded user info: {0}", res.json())

        return res.json()
