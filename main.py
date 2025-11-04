from contextlib import asynccontextmanager
import time
import uvicorn
from fastapi import FastAPI,Request
from connect import create_db_and_tables
from orm.src.backbone_orm.repository_abstract import set_global_manager
from src.routers.api_parcel import router
from fastapi.middleware.cors import CORSMiddleware
from orm.src.backbone_orm.postgres_manager import PostgresManager, ConnectionConfig
from src.models import *


async def startup_event():
    DB_CONFIG = ConnectionConfig(
        user="postgres",
        password="13801211",
        host="127.0.0.1",
        port=5432,
        db="task_shipping"
    )
    MANAGER = PostgresManager(DB_CONFIG)
    set_global_manager(MANAGER)

    try:
        await MANAGER.acquire()
        print("INFO: Database connection successfully established via PostgresManager.")
        await MANAGER.release(driver=None)
    except Exception as e:
        print(f"FATAL ERROR: Failed to acquire database connection: {e}")
        await create_db_and_tables()


@asynccontextmanager
async def lifespan(app: FastAPI):

    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.add_event_handler("startup", startup_event)
app.include_router(router)
origins = [
    # مبداهای مجاز
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await  call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
if __name__ == "__main__":
    uvicorn.run('config:app',host='0.0.0.0',port=8000,reload=True)