"""repositories.media_repository"""
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
from repositories.ig import IgBaseRepository

CONFIG = Config().config


@dataclass
class MediaRepository(IgBaseRepository):
    """media repository"""

    # TODO: rename method name
    def get_media_info(self, ig_media_id: str) -> dict:
        """get media info

        Args:
            ig_media_id (str): media id

        Raises:
            Exception: failed to request a url

        Returns:
            dict: media info
        """
        fields = "caption,comments_count,id,ig_id, like_count, media_product_type, media_type, media_url, owner, permalink, shortcode, thumbnail_url, timestamp,username"
        url = (f"{self.BASE_URL}/{self.API_VERSION}/{ig_media_id}"
               f"?fields={fields}&access_token={self.ACCESS_TOKEN}")
        debug("request media info to {0}", url)

        try:
            res = requests.get(url, timeout=30).json()
            debug("responded media info: {0}", res)
        except Exception as exc:
            error("failed to request media info. {0}: {1}", exc.__class__.__name__, exc)
            raise Exception

        return res
