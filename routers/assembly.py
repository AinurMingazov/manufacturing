from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from db_models import Assembly, AssemblyMaterial, AssemblyDetail, AssemblyStandardDetail, AssemblyLabor
from schemas import AssemblyResponse

router = APIRouter(prefix="/assembly", tags=["assembly"])


def _assembly_to_response(a: Assembly, db: Session) -> AssemblyResponse:
    materials = [r.material_id for r in db.query(AssemblyMaterial).filter(AssemblyMaterial.assembly_id == a.id).all() if r.material_id]
    details = [r.detail_id for r in db.query(AssemblyDetail).filter(AssemblyDetail.assembly_id == a.id).all() if r.detail_id]
    standard_details = [r.standard_detail_id for r in db.query(AssemblyStandardDetail).filter(AssemblyStandardDetail.assembly_id == a.id).all() if r.standard_detail_id]
    labors = [r.labor_id for r in db.query(AssemblyLabor).filter(AssemblyLabor.assembly_id == a.id).all() if r.labor_id]
    return AssemblyResponse(
        id=a.id,
        name=a.name,
        slug=a.slug,
        materials=materials,
        details=details,
        standard_details=standard_details,
        labors=labors,
    )


@router.get("/{id}", response_model=list[AssemblyResponse])
def assembly_get(id: int, db: Session = Depends(get_db)):
    items = db.query(Assembly).filter(Assembly.id == id).all()
    if not items:
        raise HTTPException(status_code=404, detail="Not found")
    return [_assembly_to_response(a, db) for a in items]
