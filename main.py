from fastapi import FastAPI

from routers import material, plan, product, assembly, detail

app = FastAPI(title="Manufacturing API")

app.include_router(material.router, prefix="/api")
app.include_router(plan.router, prefix="/api")
app.include_router(product.router, prefix="/api")
app.include_router(assembly.router, prefix="/api")
app.include_router(detail.router, prefix="/api")
