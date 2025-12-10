from pydantic import BaseModel, HttpUrl
from typing import Optional

class GoogleDriveImportRequest(BaseModel):
    folder_url: HttpUrl

class ImageBase(BaseModel):
    name: str
    google_drive_id: str
    size: Optional[int] = None
    mime_type: Optional[str] = None
    storage_path: str

class ImageOut(ImageBase):
    id: int

    class Config:
        orm_mode = True
