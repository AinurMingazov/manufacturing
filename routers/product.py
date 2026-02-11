from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from db_models import Product, ProductMaterial, ProductAssembly, ProductDetail, ProductStandardDetail, ProductLabor
from schemas import ProductResponse

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


@router.get("/{id}", response_model=list[ProductResponse])
def product_get(id: int, db: Session = Depends(get_db)):
    items = db.query(Product).filter(Product.id == id).all()
    if not items:
        raise HTTPException(status_code=404, detail="Not found")
    return [_product_to_response(p, db) for p in items]
