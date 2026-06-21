from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pytils.translit import slugify

from database import get_db
from db_models import Detail, DetailMaterial, DetailLabor
from schemas import DetailCreate, DetailUpdate, DetailResponse

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


def _apply_detail_update(obj: Detail, p: DetailUpdate, db: Session):
    if p.name is not None:
        obj.name = p.name
        obj.slug = slugify(p.name)
    if p.materials is not None:
        db.query(DetailMaterial).filter(DetailMaterial.detail_id == obj.id).delete()
        for material_id in p.materials:
            db.add(DetailMaterial(detail_id=obj.id, material_id=material_id))
    if p.labors is not None:
        db.query(DetailLabor).filter(DetailLabor.detail_id == obj.id).delete()
        for labor_id in p.labors:
            db.add(DetailLabor(detail_id=obj.id, labor_id=labor_id))


@router.get("", response_model=list[DetailResponse])
def detail_list(db: Session = Depends(get_db)):
    items = db.query(Detail).order_by(Detail.name).all()
    return [_detail_to_response(d, db) for d in items]


@router.get("/{id}", response_model=DetailResponse)
def detail_get(id: int, db: Session = Depends(get_db)):
    obj = db.query(Detail).filter(Detail.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return _detail_to_response(obj, db)


@router.post("", response_model=DetailResponse, status_code=201)
def detail_create(p: DetailCreate, db: Session = Depends(get_db)):
    obj = Detail(name=p.name, slug=slugify(p.name))
    db.add(obj)
    db.flush()
    for material_id in p.materials:
        db.add(DetailMaterial(detail_id=obj.id, material_id=material_id))
    for labor_id in p.labors:
        db.add(DetailLabor(detail_id=obj.id, labor_id=labor_id))
    db.commit()
    db.refresh(obj)
    return _detail_to_response(obj, db)


@router.put("/{id}", response_model=DetailResponse)
def detail_update(id: int, p: DetailUpdate, db: Session = Depends(get_db)):
    obj = db.query(Detail).filter(Detail.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    _apply_detail_update(obj, p, db)
    db.commit()
    db.refresh(obj)
    return _detail_to_response(obj, db)


@router.patch("/{id}", response_model=DetailResponse)
def detail_patch(id: int, p: DetailUpdate, db: Session = Depends(get_db)):
    obj = db.query(Detail).filter(Detail.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    _apply_detail_update(obj, p, db)
    db.commit()
    db.refresh(obj)
    return _detail_to_response(obj, db)


@router.delete("/{id}", status_code=204)
def detail_delete(id: int, db: Session = Depends(get_db)):
    obj = db.query(Detail).filter(Detail.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    db.query(DetailMaterial).filter(DetailMaterial.detail_id == id).delete()
    db.query(DetailLabor).filter(DetailLabor.detail_id == id).delete()
    db.delete(obj)
    db.commit()
