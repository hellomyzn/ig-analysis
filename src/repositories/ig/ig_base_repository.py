"""repositories.user_repository"""
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
from common.config import Config
from repositories.ig import IgRepositoryInterface

CONFIG = Config().config


@dataclass
class IgBaseRepository(IgRepositoryInterface):
    """user repository"""

    BASE_URL: str = field(init=False, default="https://graph.facebook.com")
    API_VERSION: str = field(init=False, default="v19.0")
    ACCESS_TOKEN: str = field(init=False, default=CONFIG["IG"]["ACCESS_TOKEN"])

    def get(self):
        pass
