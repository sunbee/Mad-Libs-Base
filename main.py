from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/')
async def root():
    return HTMLResponse("<h2>Marvellous Mavericks Make Methodical Mad-Libs</h2>")

@app.get('/item/{item_ID}')
async def getItem(item_ID: int, q: str = None):
    return {"item": item_ID, "q": q}

