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


class ManufacturingPlanResponse(BaseModel):
    id: int
    name: str
    slug: str
    products: list[int] = []
    assemblies: list[int] = []
    details: list[int] = []
    labors: list[int] = []

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    id: int
    name: str
    slug: str
    materials: list[int] = []
    assemblies: list[int] = []
    details: list[int] = []
    standard_details: list[int] = []
    labors: list[int] = []

    class Config:
        from_attributes = True


class AssemblyResponse(BaseModel):
    id: int
    name: str
    slug: str
    materials: list[int] = []
    details: list[int] = []
    standard_details: list[int] = []
    labors: list[int] = []

    class Config:
        from_attributes = True


class DetailResponse(BaseModel):
    id: int
    name: str
    slug: str
    materials: list[int] = []
    labors: list[int] = []

    class Config:
        from_attributes = True
