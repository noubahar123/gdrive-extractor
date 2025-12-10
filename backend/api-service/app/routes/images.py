from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter(tags=["Images"])

@router.get("/images", response_model=List[schemas.ImageOut])
def list_images(db: Session = Depends(get_db)):
    images = db.query(models.Image).order_by(models.Image.id.desc()).all()
    return images
