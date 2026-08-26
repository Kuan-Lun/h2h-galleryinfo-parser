# H@H Gallery Parser (h2h-galleryinfo-parser)

H@H Gallery Parser parses galleries downloaded by H@H. Each downloaded gallery
is a folder containing image files and a `galleryinfo.txt` file; this package
extracts that metadata for further use.

## Features

The package provides three core functionalities:

1. **Parse Gallery ID**: Extract the gallery ID from a given gallery folder.

2. **Gallery Information Parsing**: `GalleryInfoParser` extracts the gallery
   name, ID, modification time, title, upload and download times, comments,
   uploader account, tags, and page count. It does not retain file paths, and
   computes the page count with a constant-memory directory pass.

3. **Parse Gallery Information**: Extract all relevant folder details as a
   `GalleryInfoParser` instance.

## Installation

You can install this package using pip:

```sh
pip install h2h-galleryinfo-parser
```

## Usage

Here's a quick example of how to use H@H Gallery Parser:

```python
from pathlib import Path

from h2h_galleryinfo_parser import parse_gid, parse_galleryinfo

# Parse gallery ID from folder path
gallery_id = parse_gid(Path("/path/to/gallery/folder"))
print(f"Gallery ID: {gallery_id}")

# Parse gallery information
gallery_info = parse_galleryinfo(Path("/path/to/gallery/folder"))
print(f"Gallery Title: {gallery_info.title}")
print(f"Tags: {gallery_info.tags}")
```

## License

This project is distributed under the terms of the GNU General Public License
version 3 (GPLv3). See the included `LICENSE` file for the complete terms.
