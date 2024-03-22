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
from repositories import ModelAdapter
from repositories.ig import IgBaseRepository
from models import User

CONFIG = Config().config


@dataclass
class UserRepository(IgBaseRepository):
    """user repository"""
    IG_USER_ID: str = field(init=False, default=CONFIG["IG"]["USER_ID"])
    USER_ADAPTER = ModelAdapter(User, {
        "id": "id",
        "username": "username",
        "followers_count": "followers_count",
        "biography": "biography",
        "website": "website",
        "media_count": "media_count",
        "media": "media"
    })

    def get_user_info(self) -> User:
        """get user info

        Raises:
            RequestException: failed to request a url

        Returns:
            User: user model
        """
        fields = "biography,id,followers_count,media_count,username,website"
        url = (f"{self.BASE_URL}/{self.API_VERSION}/{self.IG_USER_ID}?"
               f"fields={fields}&access_token={self.ACCESS_TOKEN}")
        debug("request user info to {0}", url)

        try:
            res = requests.get(url, timeout=30)
        except requests.RequestException as exc:
            mes = "failed to request user info."
            error("{0} {1}: {2}", mes, exc.__class__.__name__, exc)
            raise requests.RequestException(mes) from exc

        user_dict = res.json()
        debug("responded user info: {0}", user_dict)
        if not user_dict:
            debug("user not found.")

        user = self.USER_ADAPTER.to_model(user_dict)
        return user

    def get_media(self) -> dict:
        """get media which is feed

        Raises:
            Exception: failed to request a url

        Returns:
            dict: media
        """
        url = f"{self.BASE_URL}/{self.IG_USER_ID}/media?access_token={self.ACCESS_TOKEN}"
        debug("request user media to {0}", url)

        has_next = True
        all_media = []
        while has_next:
            try:
                res = requests.get(url, timeout=30).json()
            except requests.RequestException as exc:
                mes = "failed to request user media."
                error("{0} {1}: {2}", mes, exc.__class__.__name__, exc)
                raise requests.RequestException(mes) from exc

            media = res["data"]
            debug("responded user media. {0}", len(media))
            all_media += media

            has_next = bool("next" in res["paging"].keys())
            if has_next:
                url = res["paging"]["next"]

        debug("responded user media: {0}", len(all_media))
        return all_media

    def get_insights_daily(self) -> dict:
        metric = "email_contacts,follower_count,get_directions_clicks,impressions,phone_call_clicks,profile_views,reach,text_message_clicks,website_clicks"
        period = "day"
        since = ""
        until = ""
        url = (f"{self.BASE_URL}/{self.API_VERSION}/{self.IG_USER_ID}"
               f"/insights?metric={metric}&period={period}"
               f"&since={since}&until={until}&access_token={self.ACCESS_TOKEN}")
        debug("request daily user insights to {0}", url)

        try:
            res = requests.get(url, timeout=30).json()
            debug("responded daily user insights: {0}", res)
        except Exception as exc:
            error("failed to request daily user insights. {0}: {1}", exc.__class__.__name__, exc)
            raise Exception

        for d in res["data"]:
            print(f"{d['name']}: {d['values']}")

        return res

    def get_insights_weekly(self) -> dict:
        metric = "impressions, reach"
        period = "week"
        since = ""
        until = ""
        url = (f"{self.BASE_URL}/{self.API_VERSION}/{self.IG_USER_ID}"
               f"/insights?metric={metric}&period={period}"
               f"&since={since}&until={until}&access_token={self.ACCESS_TOKEN}")
        debug("request weekly user insights to {0}", url)

        try:
            res = requests.get(url, timeout=30).json()
            debug("responded weekly user insights: {0}", res)
        except Exception as exc:
            error("failed to request weekly user insights. {0}: {1}", exc.__class__.__name__, exc)
            raise Exception

        for d in res["data"]:
            print(f"{d['name']}: {d['values']}")

        return res
