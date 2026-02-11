from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pytils.translit import slugify

from database import get_db
from db_models import Material
from schemas import MaterialCreate, MaterialUpdate, MaterialResponse

router = APIRouter(prefix="/material", tags=["material"])


@router.get("", response_model=list[MaterialResponse])
def material_list(db: Session = Depends(get_db)):
    return db.query(Material).order_by(Material.name).all()


@router.get("/{id}", response_model=MaterialResponse)
def material_get(id: int, db: Session = Depends(get_db)):
    obj = db.query(Material).filter(Material.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@router.post("", response_model=MaterialResponse, status_code=201)
def material_create(p: MaterialCreate, db: Session = Depends(get_db)):
    obj = Material(
        name=p.name,
        slug=slugify(p.name),
        unit=p.unit,
        price_per_meter=p.price_per_meter,
        price_per_ton=p.price_per_ton,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{id}", response_model=MaterialResponse)
def material_update(id: int, p: MaterialUpdate, db: Session = Depends(get_db)):
    obj = db.query(Material).filter(Material.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    if p.name is not None:
        obj.name = p.name
        obj.slug = slugify(p.name)
    if p.unit is not None:
        obj.unit = p.unit
    if p.price_per_meter is not None:
        obj.price_per_meter = p.price_per_meter
    if p.price_per_ton is not None:
        obj.price_per_ton = p.price_per_ton
    db.commit()
    db.refresh(obj)
    return obj


@router.patch("/{id}", response_model=MaterialResponse)
def material_patch(id: int, p: MaterialUpdate, db: Session = Depends(get_db)):
    obj = db.query(Material).filter(Material.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    if p.name is not None:
        obj.name = p.name
        obj.slug = slugify(p.name)
    if p.unit is not None:
        obj.unit = p.unit
    if p.price_per_meter is not None:
        obj.price_per_meter = p.price_per_meter
    if p.price_per_ton is not None:
        obj.price_per_ton = p.price_per_ton
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
def material_delete(id: int, db: Session = Depends(get_db)):
    obj = db.query(Material).filter(Material.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(obj)
    db.commit()
