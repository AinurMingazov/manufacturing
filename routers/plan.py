from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from db_models import ManufacturingPlan, MPProduct, MPAssembly, MPDetail, MPLabor
from schemas import ManufacturingPlanResponse

router = APIRouter(prefix="/plan", tags=["plan"])


def _plan_to_response(mp: ManufacturingPlan, db: Session) -> ManufacturingPlanResponse:
    products = [r.product_id for r in db.query(MPProduct).filter(MPProduct.mp_id == mp.id).all() if r.product_id]
    assemblies = [r.assembly_id for r in db.query(MPAssembly).filter(MPAssembly.mp_id == mp.id).all() if r.assembly_id]
    details = [r.detail_id for r in db.query(MPDetail).filter(MPDetail.mp_id == mp.id).all() if r.detail_id]
    labors = [r.labor_id for r in db.query(MPLabor).filter(MPLabor.mp_id == mp.id).all() if r.labor_id]
    return ManufacturingPlanResponse(
        id=mp.id,
        name=mp.name,
        slug=mp.slug,
        products=products,
        assemblies=assemblies,
        details=details,
        labors=labors,
    )


@router.get("", response_model=list[ManufacturingPlanResponse])
def plan_list(db: Session = Depends(get_db)):
    plans = db.query(ManufacturingPlan).order_by(ManufacturingPlan.name).all()
    return [_plan_to_response(p, db) for p in plans]


@router.get("/{slug}", response_model=list[ManufacturingPlanResponse])
def plan_get(slug: str, db: Session = Depends(get_db)):
    plans = db.query(ManufacturingPlan).filter(ManufacturingPlan.slug == slug).all()
    return [_plan_to_response(p, db) for p in plans]
