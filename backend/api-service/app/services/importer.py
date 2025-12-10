from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Image
from ..google_drive_client import list_image_files_in_folder


def process_google_drive_folder(folder_id: str) -> None:
    """
    Background task:
    - Lists image files from a public Google Drive folder
    - Inserts metadata into the images table
    """
    db: Session = SessionLocal()

    try:
        files = list_image_files_in_folder(folder_id)
        print(f"[API-WORKER] Found {len(files)} images in folder {folder_id}")

        for f in files:
            size_value = None
            if "size" in f:
                try:
                    size_value = int(f["size"])
                except (ValueError, TypeError):
                    size_value = None

            img = Image(
                name=f["name"],
                google_drive_id=f["id"],
                size=size_value,
                mime_type=f.get("mimeType"),
                storage_path=f"google-drive://{f['id']}",
            )

            db.add(img)

        db.commit()
        print(f"[API-WORKER] Imported {len(files)} images from folder {folder_id}")

    except Exception as e:
        db.rollback()
        print(f"[API-WORKER] Error importing folder {folder_id}: {e}")
    finally:
        db.close()
