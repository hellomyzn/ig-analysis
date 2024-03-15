"""controllers.user_controller"""
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
from services import UserService


@dataclass
class UserController(object):
    """user info controller"""
    service: UserService = field(init=False, default=UserService())

    def add(self):
        self.service.add()
