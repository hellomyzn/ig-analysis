"""services.media_service"""
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
from repositories.ig import MediaRepository
from common.config import Config

CONFIG = Config().config


@dataclass
class MediaService(object):
    """user service"""
    ig_repo: MediaRepository = field(init=True, default_factory=MediaRepository)

    # def __init__(self):
    #     self.ig_repo = MediaRepository()

    def get(self):
        ig_media_id = CONFIG["IG"]["MEDIA_ID"]
        media = self.ig_repo.get_media_info(ig_media_id)
