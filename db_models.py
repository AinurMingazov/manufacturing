from decimal import Decimal
from sqlalchemy import Column, BigInteger, String, Numeric, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Material(Base):
    __tablename__ = "cost_material"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(60), unique=True, nullable=False)
    slug = Column(String(60), unique=True, nullable=False)
    unit = Column(String(20), default="кг")
    price_per_meter = Column(Numeric(12, 2), nullable=True)
    price_per_ton = Column(Numeric(12, 2), nullable=True)


class Labor(Base):
    __tablename__ = "cost_labor"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(60), unique=True, nullable=False)
    slug = Column(String(60), unique=True, nullable=False)
    machine = Column(String(60), unique=True, nullable=False)


class StandardDetail(Base):
    __tablename__ = "cost_standard_detail"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    unit = Column(String(20), nullable=True, default="шт.")


class Detail(Base):
    __tablename__ = "cost_detail"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(60), unique=True, nullable=False)
    slug = Column(String(60), unique=True, nullable=False)


class DetailMaterial(Base):
    __tablename__ = "cost_detail_material"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    detail_id = Column(BigInteger, ForeignKey("cost_detail.id"), nullable=True)
    material_id = Column(BigInteger, ForeignKey("cost_material.id"), nullable=True)
    amount = Column(Numeric(12, 3), nullable=True)


class DetailLabor(Base):
    __tablename__ = "cost_detail_labor"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    detail_id = Column(BigInteger, ForeignKey("cost_detail.id"), nullable=True)
    labor_id = Column(BigInteger, ForeignKey("cost_labor.id"), nullable=True)
    time = Column(Numeric(12, 3), nullable=True)


class Assembly(Base):
    __tablename__ = "cost_assembly"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(60), unique=True, nullable=False)
    slug = Column(String(60), unique=True, nullable=False)


class AssemblyMaterial(Base):
    __tablename__ = "cost_assembly_material"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    assembly_id = Column(BigInteger, ForeignKey("cost_assembly.id"), nullable=True)
    material_id = Column(BigInteger, ForeignKey("cost_material.id"), nullable=True)
    amount = Column(Numeric(12, 3), nullable=True)


class AssemblyDetail(Base):
    __tablename__ = "cost_assembly_detail"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    assembly_id = Column(BigInteger, ForeignKey("cost_assembly.id"), nullable=True)
    detail_id = Column(BigInteger, ForeignKey("cost_detail.id"), nullable=True)
    amount = Column(Integer, default=1)


class AssemblyStandardDetail(Base):
    __tablename__ = "cost_assembly_standard_detail"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    assembly_id = Column(BigInteger, ForeignKey("cost_assembly.id"), nullable=True)
    standard_detail_id = Column(BigInteger, ForeignKey("cost_standard_detail.id"), nullable=True)
    amount = Column(Numeric(12, 3), nullable=True)


class AssemblyLabor(Base):
    __tablename__ = "cost_assembly_labor"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    assembly_id = Column(BigInteger, ForeignKey("cost_assembly.id"), nullable=True)
    labor_id = Column(BigInteger, ForeignKey("cost_labor.id"), nullable=True)
    time = Column(Numeric(12, 3), nullable=True)


class Product(Base):
    __tablename__ = "cost_product"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)


class ProductMaterial(Base):
    __tablename__ = "cost_product_material"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey("cost_product.id"), nullable=True)
    material_id = Column(BigInteger, ForeignKey("cost_material.id"), nullable=True)
    amount = Column(Numeric(12, 3), nullable=True)


class ProductAssembly(Base):
    __tablename__ = "cost_product_assembly"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey("cost_product.id"), nullable=True)
    assembly_id = Column(BigInteger, ForeignKey("cost_assembly.id"), nullable=True)
    amount = Column(Integer, default=1)


class ProductDetail(Base):
    __tablename__ = "cost_product_detail"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey("cost_product.id"), nullable=True)
    detail_id = Column(BigInteger, ForeignKey("cost_detail.id"), nullable=True)
    amount = Column(Integer, default=1)


class ProductStandardDetail(Base):
    __tablename__ = "cost_product_standard_detail"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey("cost_product.id"), nullable=True)
    standard_detail_id = Column(BigInteger, ForeignKey("cost_standard_detail.id"), nullable=True)
    amount = Column(Numeric(12, 3), nullable=True)


class ProductLabor(Base):
    __tablename__ = "cost_product_labor"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey("cost_product.id"), nullable=True)
    labor_id = Column(BigInteger, ForeignKey("cost_labor.id"), nullable=True)
    time = Column(Numeric(12, 3), nullable=True)


class ManufacturingPlan(Base):
    __tablename__ = "cost_manufacturing_plan"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(200), unique=True, nullable=False)
    slug = Column(String(200), unique=True, nullable=False)


class MPProduct(Base):
    __tablename__ = "cost_mp_product"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    mp_id = Column(BigInteger, ForeignKey("cost_manufacturing_plan.id"), nullable=True)
    product_id = Column(BigInteger, ForeignKey("cost_product.id"), nullable=True)
    amount = Column(Integer, default=1)


class MPAssembly(Base):
    __tablename__ = "cost_mp_assembly"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    mp_id = Column(BigInteger, ForeignKey("cost_manufacturing_plan.id"), nullable=True)
    assembly_id = Column(BigInteger, ForeignKey("cost_assembly.id"), nullable=True)
    amount = Column(Integer, default=1)


class MPDetail(Base):
    __tablename__ = "cost_mp_detail"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    mp_id = Column(BigInteger, ForeignKey("cost_manufacturing_plan.id"), nullable=True)
    detail_id = Column(BigInteger, ForeignKey("cost_detail.id"), nullable=True)
    amount = Column(Integer, default=1)


class MPLabor(Base):
    __tablename__ = "cost_mp_labor"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    mp_id = Column(BigInteger, ForeignKey("cost_manufacturing_plan.id"), nullable=True)
    labor_id = Column(BigInteger, ForeignKey("cost_labor.id"), nullable=True)
    time = Column(Numeric(12, 3), nullable=True)
