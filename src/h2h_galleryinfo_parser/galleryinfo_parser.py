__all__ = ["parse_gid", "parse_galleryinfo", "GalleryInfoParser"]


import datetime
import os
from dataclasses import dataclass, field

type GalleryTags = list[tuple[str, str]]


def count_files_in_directory(directory_path: str) -> int:
    return len(
        [
            f
            for f in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, f))
        ]
    )


@dataclass(slots=True)
class GalleryInfoParser:
    """
    A class that represents a parser for gallery information.

    Attributes:
        gallery_folder (str): The path to the gallery folder.
        gallery_name (str): The name of the gallery.
        gid (int): The gallery ID.
        files_path (list[str]): The paths of the files in the gallery.
        modified_time (datetime.datetime): The modified time of the gallery.
        title (str): The title of the gallery.
        upload_time (datetime.datetime): The upload time of the gallery.
        galleries_comments (str): The uploader's comment for the gallery.
        upload_account (str): The account used to upload the gallery.
        download_time (datetime.datetime): The download time of the gallery.
        tags (GalleryTags): The tags associated with the gallery.
        pages (int): The number of pages in the gallery.
    """

    gallery_folder: str
    gallery_name: str
    gid: int
    files_path: list[str]
    modified_time: datetime.datetime
    title: str
    upload_time: datetime.datetime
    galleries_comments: str
    upload_account: str
    download_time: datetime.datetime
    tags: GalleryTags
    _pages: int = field(default=-1, init=False, repr=False)

    @property
    def pages(self) -> int:
        if self._pages == -1:
            self._pages = count_files_in_directory(self.gallery_folder) - 1
        return self._pages


def parse_gid(gallery_folder: str) -> int:
    """
    Parses the gallery ID from the given folder path.

    Args:
        gallery_folder (str): The path to the folder containing the gallery information.

    Returns:
        int: The gallery ID.
    """
    gallery_name = os.path.basename(gallery_folder)
    if "[" in gallery_name and "]" in gallery_name:
        gid = int(gallery_name.split("[")[-1].replace("]", ""))
    else:
        gid = int(gallery_name)
    return gid


def parse_galleryinfo(gallery_folder: str) -> GalleryInfoParser:
    """
    Parses the gallery information from the given folder path.

    Args:
        gallery_folder (str): The path to the folder containing the gallery information.

    Returns:
        GalleryInfoParser: An instance of the GalleryInfoParser class containing
            the parsed gallery information.
    """
    gallery_info_path = os.path.join(gallery_folder, "galleryinfo.txt")
    with open(gallery_info_path, encoding="utf-8") as file:
        lines = file.read().strip("\n").split("\n")

    gallery_name = os.path.basename(gallery_folder)
    gid = parse_gid(gallery_folder)
    files_path = os.listdir(gallery_folder)
    modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(gallery_info_path))

    comments = False
    comment_lines: list[str] = []
    for line in lines:
        if "Uploader's Comments" in line:
            comments = True
        elif comments:
            if (
                line
                == "Downloaded from E-Hentai Galleries by the Hentai@Home Downloader <3"
            ):
                break
            comment_lines.append(line.strip())
        elif ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            match key:
                case "Tags":
                    tags: GalleryTags = []
                    for tag in value.split(","):
                        if ":" in tag:
                            tag_key, tag_value = tag.split(":", 1)
                            if tag_key.strip() != "":
                                tags.append((tag_key.strip(), tag_value.strip()))
                            else:
                                tags.append(("untagged", tag_value.strip()))
                        else:
                            tags.append(("untagged", tag.strip()))
                case "Title":
                    title = value
                case "Upload Time":
                    upload_time = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M")
                case "Uploaded By":
                    upload_account = value
                case "Downloaded":
                    download_time = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M")

    galleries_comments = "\n".join(comment_lines).strip("\n")

    return GalleryInfoParser(
        gallery_folder=gallery_folder,
        gallery_name=gallery_name,
        gid=gid,
        files_path=files_path,
        modified_time=modified_time,
        title=title,
        upload_time=upload_time,
        galleries_comments=galleries_comments,
        upload_account=upload_account,
        download_time=download_time,
        tags=tags,
    )
