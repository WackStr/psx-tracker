from fastapi import FastAPI

app = FastAPI()

@app.get("/share-price/{script}")
async def get_share_price(script: str):
    """get_price_of_share"""
    return {"share-price": 10.0}