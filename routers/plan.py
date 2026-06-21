from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pytils.translit import slugify

from database import get_db
from db_models import ManufacturingPlan, MPProduct, MPAssembly, MPDetail, MPLabor
from schemas import ManufacturingPlanCreate, ManufacturingPlanUpdate, ManufacturingPlanResponse

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


def _apply_plan_update(obj: ManufacturingPlan, p: ManufacturingPlanUpdate, db: Session):
    if p.name is not None:
        obj.name = p.name
        obj.slug = slugify(p.name)
    if p.products is not None:
        db.query(MPProduct).filter(MPProduct.mp_id == obj.id).delete()
        for product_id in p.products:
            db.add(MPProduct(mp_id=obj.id, product_id=product_id))
    if p.assemblies is not None:
        db.query(MPAssembly).filter(MPAssembly.mp_id == obj.id).delete()
        for assembly_id in p.assemblies:
            db.add(MPAssembly(mp_id=obj.id, assembly_id=assembly_id))
    if p.details is not None:
        db.query(MPDetail).filter(MPDetail.mp_id == obj.id).delete()
        for detail_id in p.details:
            db.add(MPDetail(mp_id=obj.id, detail_id=detail_id))
    if p.labors is not None:
        db.query(MPLabor).filter(MPLabor.mp_id == obj.id).delete()
        for labor_id in p.labors:
            db.add(MPLabor(mp_id=obj.id, labor_id=labor_id))


@router.get("", response_model=list[ManufacturingPlanResponse])
def plan_list(db: Session = Depends(get_db)):
    plans = db.query(ManufacturingPlan).order_by(ManufacturingPlan.name).all()
    return [_plan_to_response(p, db) for p in plans]


@router.get("/slug/{slug}", response_model=list[ManufacturingPlanResponse])
def plan_get_by_slug(slug: str, db: Session = Depends(get_db)):
    plans = db.query(ManufacturingPlan).filter(ManufacturingPlan.slug == slug).all()
    return [_plan_to_response(p, db) for p in plans]


@router.get("/{id}", response_model=ManufacturingPlanResponse)
def plan_get(id: int, db: Session = Depends(get_db)):
    obj = db.query(ManufacturingPlan).filter(ManufacturingPlan.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return _plan_to_response(obj, db)


@router.post("", response_model=ManufacturingPlanResponse, status_code=201)
def plan_create(p: ManufacturingPlanCreate, db: Session = Depends(get_db)):
    obj = ManufacturingPlan(name=p.name, slug=slugify(p.name))
    db.add(obj)
    db.flush()
    for product_id in p.products:
        db.add(MPProduct(mp_id=obj.id, product_id=product_id))
    for assembly_id in p.assemblies:
        db.add(MPAssembly(mp_id=obj.id, assembly_id=assembly_id))
    for detail_id in p.details:
        db.add(MPDetail(mp_id=obj.id, detail_id=detail_id))
    for labor_id in p.labors:
        db.add(MPLabor(mp_id=obj.id, labor_id=labor_id))
    db.commit()
    db.refresh(obj)
    return _plan_to_response(obj, db)


@router.put("/{id}", response_model=ManufacturingPlanResponse)
def plan_update(id: int, p: ManufacturingPlanUpdate, db: Session = Depends(get_db)):
    obj = db.query(ManufacturingPlan).filter(ManufacturingPlan.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    _apply_plan_update(obj, p, db)
    db.commit()
    db.refresh(obj)
    return _plan_to_response(obj, db)


@router.patch("/{id}", response_model=ManufacturingPlanResponse)
def plan_patch(id: int, p: ManufacturingPlanUpdate, db: Session = Depends(get_db)):
    obj = db.query(ManufacturingPlan).filter(ManufacturingPlan.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    _apply_plan_update(obj, p, db)
    db.commit()
    db.refresh(obj)
    return _plan_to_response(obj, db)


@router.delete("/{id}", status_code=204)
def plan_delete(id: int, db: Session = Depends(get_db)):
    obj = db.query(ManufacturingPlan).filter(ManufacturingPlan.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    db.query(MPProduct).filter(MPProduct.mp_id == id).delete()
    db.query(MPAssembly).filter(MPAssembly.mp_id == id).delete()
    db.query(MPDetail).filter(MPDetail.mp_id == id).delete()
    db.query(MPLabor).filter(MPLabor.mp_id == id).delete()
    db.delete(obj)
    db.commit()
