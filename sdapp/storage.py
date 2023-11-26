import pathlib

from fastapi import Request
from PIL.Image import Image

from sdapp.logger import logger
from sdapp.settings import settings

STATIC_ROOT = pathlib.Path(__file__).resolve().parent / "static"


class Storage:
    def __init__(self, path: str = settings.static_dir):
        self.path = STATIC_ROOT

    def upload_image(self, image: Image, file_name: str):
        try:
            image.save(self.path / file_name, format="PNG")
            logger.info("Image", file_name, "was uploaded successfully")

        except Exception as e:
            logger.error("Error in file upload", e)

    def get_url(self, request: Request, file_name: str):
        return f"{request.base_url}static/{file_name}"
