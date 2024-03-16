"""controllers.media_controller"""
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
from services import MediaService


@dataclass
class MediaController(object):
    """user info controller"""
    service: MediaService = field(init=True, default_factory=MediaService)

    # def __init__(self):
    #     self.service = MediaService()

    def get(self):
        """_summary_
        """
        self.service.get()
