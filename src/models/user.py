"""models.user"""
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
class User(Model):
    """user data class"""
    id: int | None = field(init=True, default=None)
    username: str | None = field(init=True, default=None)
    followers_count: int | None = field(init=True, default=None)
    media_count: int | None = field(init=True, default=None)
    biography: str | None = field(init=True, default=None)
    website: str | None = field(init=True, default=None)

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
            "username": dict_.get("username"),
            "followers_count": dict_.get("followers_count"),
            "media_count": dict_.get("media_count"),
            "biography": dict_.get("biography"),
            "website": dict_.get("website"),
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
            "username": self.username,
            "followers_count": self.followers_count,
            "media_count": self.media_count,
            "biography": self.biography,
            "website": self.website
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
