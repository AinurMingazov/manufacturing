from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class MaterialBase(BaseModel):
    name: str
    unit: str = "кг"
    price_per_meter: Optional[Decimal] = None
    price_per_ton: Optional[Decimal] = None


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(MaterialBase):
    name: Optional[str] = None
    unit: Optional[str] = None


class MaterialResponse(MaterialBase):
    id: int
    slug: str

    class Config:
        from_attributes = True


class ManufacturingPlanBase(BaseModel):
    name: str
    products: list[int] = []
    assemblies: list[int] = []
    details: list[int] = []
    labors: list[int] = []


class ManufacturingPlanCreate(ManufacturingPlanBase):
    pass


class ManufacturingPlanUpdate(BaseModel):
    name: Optional[str] = None
    products: Optional[list[int]] = None
    assemblies: Optional[list[int]] = None
    details: Optional[list[int]] = None
    labors: Optional[list[int]] = None


class ManufacturingPlanResponse(ManufacturingPlanBase):
    id: int
    slug: str

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    materials: list[int] = []
    assemblies: list[int] = []
    details: list[int] = []
    standard_details: list[int] = []
    labors: list[int] = []


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    materials: Optional[list[int]] = None
    assemblies: Optional[list[int]] = None
    details: Optional[list[int]] = None
    standard_details: Optional[list[int]] = None
    labors: Optional[list[int]] = None


class ProductResponse(ProductBase):
    id: int
    slug: str

    class Config:
        from_attributes = True


class AssemblyBase(BaseModel):
    name: str
    materials: list[int] = []
    details: list[int] = []
    standard_details: list[int] = []
    labors: list[int] = []


class AssemblyCreate(AssemblyBase):
    pass


class AssemblyUpdate(BaseModel):
    name: Optional[str] = None
    materials: Optional[list[int]] = None
    details: Optional[list[int]] = None
    standard_details: Optional[list[int]] = None
    labors: Optional[list[int]] = None


class AssemblyResponse(AssemblyBase):
    id: int
    slug: str

    class Config:
        from_attributes = True


class DetailBase(BaseModel):
    name: str
    materials: list[int] = []
    labors: list[int] = []


class DetailCreate(DetailBase):
    pass


class DetailUpdate(BaseModel):
    name: Optional[str] = None
    materials: Optional[list[int]] = None
    labors: Optional[list[int]] = None


class DetailResponse(DetailBase):
    id: int
    slug: str

    class Config:
        from_attributes = True
