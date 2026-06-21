from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pytils.translit import slugify

from database import get_db
from db_models import Product, ProductMaterial, ProductAssembly, ProductDetail, ProductStandardDetail, ProductLabor
from schemas import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/product", tags=["product"])


def _product_to_response(p: Product, db: Session) -> ProductResponse:
    materials = [r.material_id for r in db.query(ProductMaterial).filter(ProductMaterial.product_id == p.id).all() if r.material_id]
    assemblies = [r.assembly_id for r in db.query(ProductAssembly).filter(ProductAssembly.product_id == p.id).all() if r.assembly_id]
    details = [r.detail_id for r in db.query(ProductDetail).filter(ProductDetail.product_id == p.id).all() if r.detail_id]
    standard_details = [r.standard_detail_id for r in db.query(ProductStandardDetail).filter(ProductStandardDetail.product_id == p.id).all() if r.standard_detail_id]
    labors = [r.labor_id for r in db.query(ProductLabor).filter(ProductLabor.product_id == p.id).all() if r.labor_id]
    return ProductResponse(
        id=p.id,
        name=p.name,
        slug=p.slug,
        materials=materials,
        assemblies=assemblies,
        details=details,
        standard_details=standard_details,
        labors=labors,
    )


def _apply_product_update(obj: Product, p: ProductUpdate, db: Session):
    if p.name is not None:
        obj.name = p.name
        obj.slug = slugify(p.name)
    if p.materials is not None:
        db.query(ProductMaterial).filter(ProductMaterial.product_id == obj.id).delete()
        for material_id in p.materials:
            db.add(ProductMaterial(product_id=obj.id, material_id=material_id))
    if p.assemblies is not None:
        db.query(ProductAssembly).filter(ProductAssembly.product_id == obj.id).delete()
        for assembly_id in p.assemblies:
            db.add(ProductAssembly(product_id=obj.id, assembly_id=assembly_id))
    if p.details is not None:
        db.query(ProductDetail).filter(ProductDetail.product_id == obj.id).delete()
        for detail_id in p.details:
            db.add(ProductDetail(product_id=obj.id, detail_id=detail_id))
    if p.standard_details is not None:
        db.query(ProductStandardDetail).filter(ProductStandardDetail.product_id == obj.id).delete()
        for standard_detail_id in p.standard_details:
            db.add(ProductStandardDetail(product_id=obj.id, standard_detail_id=standard_detail_id))
    if p.labors is not None:
        db.query(ProductLabor).filter(ProductLabor.product_id == obj.id).delete()
        for labor_id in p.labors:
            db.add(ProductLabor(product_id=obj.id, labor_id=labor_id))


@router.get("", response_model=list[ProductResponse])
def product_list(db: Session = Depends(get_db)):
    items = db.query(Product).order_by(Product.name).all()
    return [_product_to_response(p, db) for p in items]


@router.get("/{id}", response_model=ProductResponse)
def product_get(id: int, db: Session = Depends(get_db)):
    obj = db.query(Product).filter(Product.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return _product_to_response(obj, db)


@router.post("", response_model=ProductResponse, status_code=201)
def product_create(p: ProductCreate, db: Session = Depends(get_db)):
    obj = Product(name=p.name, slug=slugify(p.name))
    db.add(obj)
    db.flush()
    for material_id in p.materials:
        db.add(ProductMaterial(product_id=obj.id, material_id=material_id))
    for assembly_id in p.assemblies:
        db.add(ProductAssembly(product_id=obj.id, assembly_id=assembly_id))
    for detail_id in p.details:
        db.add(ProductDetail(product_id=obj.id, detail_id=detail_id))
    for standard_detail_id in p.standard_details:
        db.add(ProductStandardDetail(product_id=obj.id, standard_detail_id=standard_detail_id))
    for labor_id in p.labors:
        db.add(ProductLabor(product_id=obj.id, labor_id=labor_id))
    db.commit()
    db.refresh(obj)
    return _product_to_response(obj, db)


@router.put("/{id}", response_model=ProductResponse)
def product_update(id: int, p: ProductUpdate, db: Session = Depends(get_db)):
    obj = db.query(Product).filter(Product.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    _apply_product_update(obj, p, db)
    db.commit()
    db.refresh(obj)
    return _product_to_response(obj, db)


@router.patch("/{id}", response_model=ProductResponse)
def product_patch(id: int, p: ProductUpdate, db: Session = Depends(get_db)):
    obj = db.query(Product).filter(Product.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    _apply_product_update(obj, p, db)
    db.commit()
    db.refresh(obj)
    return _product_to_response(obj, db)


@router.delete("/{id}", status_code=204)
def product_delete(id: int, db: Session = Depends(get_db)):
    obj = db.query(Product).filter(Product.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    db.query(ProductMaterial).filter(ProductMaterial.product_id == id).delete()
    db.query(ProductAssembly).filter(ProductAssembly.product_id == id).delete()
    db.query(ProductDetail).filter(ProductDetail.product_id == id).delete()
    db.query(ProductStandardDetail).filter(ProductStandardDetail.product_id == id).delete()
    db.query(ProductLabor).filter(ProductLabor.product_id == id).delete()
    db.delete(obj)
    db.commit()
