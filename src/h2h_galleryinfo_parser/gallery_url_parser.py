__all__ = ["GalleryURLParser"]


import re
from dataclasses import dataclass, field


@dataclass(slots=True)
class GalleryURLParser:
    """
    A parser for extracting gallery information from URLs of exhentai.org and
    e-hentai.org.
    Attributes:
        url (str): The original URL provided.
        gid (int): The gallery ID extracted from the URL.
        url_key (str): The URL key extracted from the URL.
    Raises:
        ValueError: If the URL is empty or not a valid gallery URL.
    """

    url: str
    gid: int = field(init=False)
    url_key: str = field(init=False)

    def __post_init__(self) -> None:
        if self.url == "":
            raise ValueError("The url cannot be empty.")

        if ("exhentai.org" not in self.url) and ("e-hentai.org" not in self.url):
            raise ValueError("The url is not the gallery's url.")

        match = None
        if "exhentai.org" in self.url:
            match = re.search(r"https://exhentai\.org/g/(\d+)/([a-zA-Z0-9]+)", self.url)
        if "e-hentai.org" in self.url:
            match = re.search(r"https://e-hentai\.org/g/(\d+)/([a-zA-Z0-9]+)", self.url)

        if not match:
            raise ValueError("The url is not the gallery's url.")
        self.gid = int(match.group(1))
        self.url_key = match.group(2)
