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
from common.log import debug, error
from common.config import Config
from repositories.ig import IgBaseRepository

CONFIG = Config().config


@dataclass
class UserRepository(IgBaseRepository):
    """user repository"""
    IG_USER_ID: str = field(init=False, default=CONFIG["IG"]["USER_ID"])
    FIELDS: str = field(init=False, default="biography,id,followers_count,media_count,username,website")

    def get(self) -> dict:
        """get user info

        Raises:
            Exception: failed to request a url

        Returns:
            dict: user info
        """
        url = (f"{self.BASE_URL}/{self.API_VERSION}/{self.IG_USER_ID}?"
               f"fields={self.FIELDS}&access_token={self.ACCESS_TOKEN}")
        debug("request user info to {0}", url)

        try:
            res = requests.get(url, timeout=30)
            debug("responded user info: {0}", res.json())
        except Exception as exc:
            error("failed to request user info. {0}: {1}", exc.__class__.__name__, exc)
            raise Exception

        return res.json()

    def get_media(self) -> dict:
        """get media which is feed

        Raises:
            Exception: failed to request a url

        Returns:
            dict: media
        """
        url = f"{self.BASE_URL}/{self.IG_USER_ID}/media?access_token={self.ACCESS_TOKEN}"
        debug("request media to {0}", url)

        has_next = True
        all_media = []
        while has_next:
            try:
                res = requests.get(url, timeout=30).json()
            except Exception as exc:
                error("failed to request media. {0}: {1}", exc.__class__.__name__, exc)
                raise Exception

            media = res["data"]
            debug("responded media. {0}", len(media))
            all_media += media

            has_next = bool("next" in res["paging"].keys())
            if has_next:
                url = res["paging"]["next"]

        debug("responded total media: {0}", len(all_media))
        return all_media
