"""models.users.user_insights"""
#########################################################
# Builtin packages
#########################################################
import json
from dataclasses import dataclass, field

#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
from models import Model


@dataclass
class UserInsights(Model):
    """user data class
        https://developers.facebook.com/docs/instagram-api/reference/ig-user/insights?locale=ja_JP
    """
    id: int | None = field(init=True, default=None)
    email_contacts: str | None = field(init=True, default=None)
    follower_count: int | None = field(init=True, default=None)
    get_directions_clicks: int | None = field(init=True, default=None)
    impressions: str | None = field(init=True, default=None)
    phone_call_clicks: str | None = field(init=True, default=None)
    profile_views: str | None = field(init=True, default=None)
    reach: str | None = field(init=True, default=None)
    text_message_clicks: str | None = field(init=True, default=None)
    website_clicks: str | None = field(init=True, default=None)
    end_time: str | None = field(init=True, default=None)

    @classmethod
    def from_dict(cls, dict_: dict):
        """convert from dict to model

        Args:
            dict_ (dict): dict data

        Returns:
            user: model
        """
        return cls(**{
            "id": dict_.get("id"),
            "email_contacts": dict_.get("email_contacts"),
            "follower_count": dict_.get("follower_count"),
            "get_directions_clicks": dict_.get("get_directions_clicks"),
            "impressions": dict_.get("impressions"),
            "phone_call_clicks": dict_.get("phone_call_clicks"),
            "profile_views": dict_.get("profile_views"),
            "reach": dict_.get("reach"),
            "text_message_clicks": dict_.get("text_message_clicks"),
            "website_clicks": dict_.get("website_clicks"),
            "end_time": dict_.get("end_time"),
        })

    def to_dict(self, without_none_field: bool = False) -> dict:
        """convert from model to dict

        Args:
            without_none_field (bool, optional): option to remove none fields. Defaults to False.

        Returns:
            dict: dict data
        """
        dict_ = {
            "id": self.id,
            "email_contacts": self.email_contacts,
            "follower_count": self.follower_count,
            "get_directions_clicks": self.get_directions_clicks,
            "impressions": self.impressions,
            "phone_call_clicks": self.phone_call_clicks,
            "profile_views": self.profile_views,
            "reach": self.reach,
            "text_message_clicks": self.text_message_clicks,
            "website_clicks": self.website_clicks,
            "end_time": self.end_time
        }

        if without_none_field:
            return {key: value for key, value in dict_.items() if value is not None}

        return dict_

    def to_json(self) -> str:
        """convert from model to json

        Returns:
            json: json data
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
