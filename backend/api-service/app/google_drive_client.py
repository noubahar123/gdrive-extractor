import os
from typing import List, Dict
from googleapiclient.discovery import build

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")


def get_drive_service():
    if not API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is not set in .env")

    service = build("drive", "v3", developerKey=API_KEY)
    return service


def list_image_files_in_folder(folder_id: str) -> List[Dict]:
    service = get_drive_service()

    # Same logic as worker: list all children, filter images
    query = f"'{folder_id}' in parents and trashed = false"

    files: List[Dict] = []
    page_token = None

    while True:
        response = (
            service.files()
            .list(
                q=query,
                fields="nextPageToken, files(id, name, mimeType, size)",
                pageToken=page_token,
                pageSize=1000,
            )
            .execute()
        )

        batch = response.get("files", [])
        files.extend(batch)
        page_token = response.get("nextPageToken")

        if not page_token:
            break

    # Filter only images
    image_files = [f for f in files if f.get("mimeType", "").startswith("image/")]

    return image_files
