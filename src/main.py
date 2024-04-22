import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_client import make_asgi_app, CollectorRegistry, Gauge, push_to_gateway

from src.ping import do_one


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting up..")
    yield
    print("Application shutting down..")
    registry = CollectorRegistry()
    g = Gauge('job_last_success_unixtime', 'Last time a batch job successfully finished', registry=registry)
    g.set_to_current_time()
    push_to_gateway('localhost:9091', job='batchA', registry=registry)


app = FastAPI(lifespan=lifespan)
# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/status/{service}")
async def status(service: str):
    for i in range(5):
        do_one(service)
        time.sleep(0.1)
