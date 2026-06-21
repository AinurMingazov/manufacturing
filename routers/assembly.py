from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pytils.translit import slugify

from database import get_db
from db_models import Assembly, AssemblyMaterial, AssemblyDetail, AssemblyStandardDetail, AssemblyLabor
from schemas import AssemblyCreate, AssemblyUpdate, AssemblyResponse

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


def _apply_assembly_update(obj: Assembly, p: AssemblyUpdate, db: Session):
    if p.name is not None:
        obj.name = p.name
        obj.slug = slugify(p.name)
    if p.materials is not None:
        db.query(AssemblyMaterial).filter(AssemblyMaterial.assembly_id == obj.id).delete()
        for material_id in p.materials:
            db.add(AssemblyMaterial(assembly_id=obj.id, material_id=material_id))
    if p.details is not None:
        db.query(AssemblyDetail).filter(AssemblyDetail.assembly_id == obj.id).delete()
        for detail_id in p.details:
            db.add(AssemblyDetail(assembly_id=obj.id, detail_id=detail_id))
    if p.standard_details is not None:
        db.query(AssemblyStandardDetail).filter(AssemblyStandardDetail.assembly_id == obj.id).delete()
        for standard_detail_id in p.standard_details:
            db.add(AssemblyStandardDetail(assembly_id=obj.id, standard_detail_id=standard_detail_id))
    if p.labors is not None:
        db.query(AssemblyLabor).filter(AssemblyLabor.assembly_id == obj.id).delete()
        for labor_id in p.labors:
            db.add(AssemblyLabor(assembly_id=obj.id, labor_id=labor_id))


@router.get("", response_model=list[AssemblyResponse])
def assembly_list(db: Session = Depends(get_db)):
    items = db.query(Assembly).order_by(Assembly.name).all()
    return [_assembly_to_response(a, db) for a in items]


@router.get("/{id}", response_model=AssemblyResponse)
def assembly_get(id: int, db: Session = Depends(get_db)):
    obj = db.query(Assembly).filter(Assembly.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return _assembly_to_response(obj, db)


@router.post("", response_model=AssemblyResponse, status_code=201)
def assembly_create(p: AssemblyCreate, db: Session = Depends(get_db)):
    obj = Assembly(name=p.name, slug=slugify(p.name))
    db.add(obj)
    db.flush()
    for material_id in p.materials:
        db.add(AssemblyMaterial(assembly_id=obj.id, material_id=material_id))
    for detail_id in p.details:
        db.add(AssemblyDetail(assembly_id=obj.id, detail_id=detail_id))
    for standard_detail_id in p.standard_details:
        db.add(AssemblyStandardDetail(assembly_id=obj.id, standard_detail_id=standard_detail_id))
    for labor_id in p.labors:
        db.add(AssemblyLabor(assembly_id=obj.id, labor_id=labor_id))
    db.commit()
    db.refresh(obj)
    return _assembly_to_response(obj, db)


@router.put("/{id}", response_model=AssemblyResponse)
def assembly_update(id: int, p: AssemblyUpdate, db: Session = Depends(get_db)):
    obj = db.query(Assembly).filter(Assembly.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    _apply_assembly_update(obj, p, db)
    db.commit()
    db.refresh(obj)
    return _assembly_to_response(obj, db)


@router.patch("/{id}", response_model=AssemblyResponse)
def assembly_patch(id: int, p: AssemblyUpdate, db: Session = Depends(get_db)):
    obj = db.query(Assembly).filter(Assembly.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    _apply_assembly_update(obj, p, db)
    db.commit()
    db.refresh(obj)
    return _assembly_to_response(obj, db)


@router.delete("/{id}", status_code=204)
def assembly_delete(id: int, db: Session = Depends(get_db)):
    obj = db.query(Assembly).filter(Assembly.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    db.query(AssemblyMaterial).filter(AssemblyMaterial.assembly_id == id).delete()
    db.query(AssemblyDetail).filter(AssemblyDetail.assembly_id == id).delete()
    db.query(AssemblyStandardDetail).filter(AssemblyStandardDetail.assembly_id == id).delete()
    db.query(AssemblyLabor).filter(AssemblyLabor.assembly_id == id).delete()
    db.delete(obj)
    db.commit()
