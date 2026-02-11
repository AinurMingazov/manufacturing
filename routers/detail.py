from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from db_models import Detail, DetailMaterial, DetailLabor
from schemas import DetailResponse

router = APIRouter(prefix="/detail", tags=["detail"])


def _detail_to_response(d: Detail, db: Session) -> DetailResponse:
    materials = [r.material_id for r in db.query(DetailMaterial).filter(DetailMaterial.detail_id == d.id).all() if r.material_id]
    labors = [r.labor_id for r in db.query(DetailLabor).filter(DetailLabor.detail_id == d.id).all() if r.labor_id]
    return DetailResponse(
        id=d.id,
        name=d.name,
        slug=d.slug,
        materials=materials,
        labors=labors,
    )


@router.get("/{id}", response_model=list[DetailResponse])
def detail_get(id: int, db: Session = Depends(get_db)):
    items = db.query(Detail).filter(Detail.id == id).all()
    if not items:
        raise HTTPException(status_code=404, detail="Not found")
    return [_detail_to_response(d, db) for d in items]
