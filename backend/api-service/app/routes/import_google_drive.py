from ..queues import enqueue_google_drive_import
from fastapi import APIRouter, HTTPException, BackgroundTasks
from urllib.parse import urlparse, parse_qs
import uuid

from ..schemas import GoogleDriveImportRequest
from ..services.importer import process_google_drive_folder

router = APIRouter(tags=["Import"])


def extract_folder_id_from_url(folder_url: str) -> str:
    parsed = urlparse(folder_url)

    # case 1: /drive/folders/<id>
    if "folders" in parsed.path:
        parts = [p for p in parsed.path.split("/") if p]
        if "folders" in parts:
            idx = parts.index("folders")
            if idx + 1 < len(parts):
                return parts[idx + 1]

    # case 2: ?id=<id>
    qs = parse_qs(parsed.query)
    if "id" in qs and qs["id"]:
        return qs["id"][0]

    raise ValueError("Could not extract Google Drive folder ID from URL.")


@router.post("/import/google-drive")
def import_google_drive_folder(payload: GoogleDriveImportRequest):
    """
    Accepts a Google Drive folder URL, extracts folder ID,
    and enqueues a Redis/RQ job for the worker service.
    """
    try:
        folder_id = extract_folder_id_from_url(str(payload.folder_url))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    job_id = enqueue_google_drive_import(folder_id)

    return {
        "message": "Import job enqueued",
        "job_id": job_id,
        "folder_id": folder_id,
    }