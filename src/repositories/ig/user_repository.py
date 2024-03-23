"""repositories.user_repository"""
#########################################################
# Builtin packages
#########################################################
import requests
from datetime import datetime, timedelta
from dataclasses import dataclass, field

#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
from common.log import debug, warn, error
from common.config import Config
from repositories import ModelAdapter
from repositories.ig import IgBaseRepository
from models.users import User
from models.users import UserInsights
from utils import DatetimeParser

CONFIG = Config().config


@dataclass
class UserRepository(IgBaseRepository):
    """user repository"""
    IG_USER_ID: str = field(init=False, default=CONFIG["IG"]["USER_ID"])
    user_adapter = ModelAdapter(User, {
        "id": "id",
        "username": "username",
        "followers_count": "followers_count",
        "biography": "biography",
        "website": "website",
        "media_count": "media_count"
    })
    insights_adapter = ModelAdapter(UserInsights, {
        "email_contacts": "email_contacts",
        "follower_count": "follower_count",
        "get_directions_clicks": "get_directions_clicks",
        "impressions": "impressions",
        "phone_call_clicks": "phone_call_clicks",
        "profile_views": "profile_views",
        "reach": "reach",
        "text_message_clicks": "text_message_clicks",
        "website_clicks": "website_clicks",
        "end_time": "end_time"
    })

    def get_user_info(self) -> User | None:
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
            debug("user info is not found.")

        user = self.user_adapter.to_model(user_dict)
        return user

    def get_insights_daily(self,
                           since: datetime | None = None,
                           until: datetime | None = None) -> list[UserInsights,] | None:
        """get user insights only Compatible Period	is day

            until datetime should be grater than since datetime.
            since and until datetime supports querying data for
            the last 30 days excluding the current day
            date difference between since and until should be less than 30 days.

        Args:
            since (datetime | None, optional): since datetime. Defaults to None.
            until (datetime | None, optional): until datetime. Defaults to None.

        Raises:
            Exception: until datetime is not grater than since datetime
            RequestException: failed to request a url

        Returns:
            list[UserInsights,] | None: list of UserInsights
        """
        # validate
        if until is None:
            until = datetime.today()
        until_ut = DatetimeParser.encode_to_unix_timestamp(until)

        if since is None:
            since = until - timedelta(days=1)
        since_ut = DatetimeParser.encode_to_unix_timestamp(since)

        if until_ut < since_ut:
            mes = "until datetime is not grater than since datetime."
            warn(mes)
            raise Exception(mes)

        # prepare
        metric = ("email_contacts,follower_count,get_directions_clicks,impressions,"
                  "phone_call_clicks,profile_views,reach,text_message_clicks,"
                  "website_clicks")
        period = "day"
        url = (f"{self.BASE_URL}/{self.API_VERSION}/{self.IG_USER_ID}"
               f"/insights?metric={metric}&period={period}"
               f"&since={since_ut}&until={until_ut}&access_token={self.ACCESS_TOKEN}")
        debug("request daily user insights to {0} since: {1}, until: {2}",
              url, since, until)

        # request
        try:
            res = requests.get(url, timeout=30).json()
            insights_list = res["data"]
        except KeyError as exc:
            mes = "data doesn't exist."
            error("{0} {1}: {2}. response: {3}",
                  mes, exc.__class__.__name__, exc, res)
            raise KeyError(mes) from exc
        except requests.RequestException as exc:
            mes = "failed to request daily user insights."
            error("{0} {1}: {2}", mes, exc.__class__.__name__, exc)
            raise requests.RequestException(mes) from exc

        if not insights_list:
            mes = "daily user insights is not found."
            debug(mes)
            return None
        debug("responded daily user insight: {0}", insights_list)

        # convert to model
        date_diff = len(insights_list[0]["values"])
        insights = []
        for num in range(date_diff):
            insights_dict = {}
            for insight in insights_list:
                name = insight["name"]
                value = insight["values"][num]["value"]
                insights_dict[name] = value
            # TODO: タイムゾーンをJST、datetime型にして、CSVに書き込む時にどういう値になるか検証する
            end_time_iso = insights_list[0]["values"][num]["end_time"]
            end_time_dt = DatetimeParser.decode_from_iso_format(end_time_iso)
            end_time_iso_ja = DatetimeParser.encode_to_iso_format(end_time_dt)
            insights_dict["end_time"] = end_time_iso_ja
            insight = self.insights_adapter.to_model(insights_dict)
            insights.append(insight)
            print(insight)
        return insights

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
