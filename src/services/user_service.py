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


@dataclass
class UserService(object):
    """user service"""
    ig_repo: UserRepository = field(init=True, default_factory=None)

    def __init__(self):
        self.ig_repo = UserRepository()

    def add(self):
        """add user info to repo
        """
        user_info = self.ig_repo.get()
