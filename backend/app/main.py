from fastapi import FastAPI
from app.core.database import engine
from sqlmodel import SQLModel
from app.core.exceptions import AppException
from fastapi.responses import JSONResponse
from fastapi import Request

from app.routers import products, warehouses, inventory, reports, auth, alerts

app = FastAPI(title="Inventory Management System")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )

app.include_router(products.router)
app.include_router(warehouses.router)
app.include_router(inventory.router)
app.include_router(reports.router)
app.include_router(auth.router)
app.include_router(alerts.router)
