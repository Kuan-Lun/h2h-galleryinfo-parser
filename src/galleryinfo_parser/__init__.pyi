class GalleryInfoParser:
    def __init__(
        self,
        gallery_folder: str,
        gallery_name: str,
        gid: int,
        files_path: list[str],
        modified_time: str,
        title: str,
        upload_time: str,
        galleries_comments: str,
        upload_account: str,
        download_time: str,
        tags: list[tuple[str, str]],
    ) -> None: ...
    def pages(self) -> int: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...

def parse_gid(gallery_folder: str) -> int: ...
def parse_galleryinfo(gallery_folder: str) -> GalleryInfoParser: ...
