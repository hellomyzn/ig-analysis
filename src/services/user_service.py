"""services.user_service"""
#########################################################
# Builtin packages
#########################################################
from dataclasses import dataclass, field

#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
from repositories.ig import UserRepository
from utils import DatetimeParser


@dataclass
class UserService(object):
    """user service"""
    ig_repo: UserRepository = field(init=True, default_factory=None)

    def __init__(self):
        self.ig_repo = UserRepository()

    def add(self):
        """add user info to repo
        """
        user_info = self.ig_repo.get_user_info()

    def get_media(self):
        media = self.ig_repo.get_media()

    def get_insights(self):
        since = "2024-03-20"
        until = "2024-03-21"
        since = None
        until = None
        since_dt = DatetimeParser.decode_from_str_date(since)
        until_dt = DatetimeParser.decode_from_str_date(until)
        media = self.ig_repo.get_insights_daily(since=since_dt, until=until_dt)
