from fastapi import FastAPI
from src.ping import do_one

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/status/{service}")
def status(service: str):
    print("?????", service)
    return do_one(service)
