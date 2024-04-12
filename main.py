import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

from route.router import USER_ROUTER, AUTH_ROUTER
from database.create_session import Base, engine


app = FastAPI()

app.include_router(router=USER_ROUTER)
app.include_router(router=AUTH_ROUTER)

# Create Database
Base.metadata.create_all(bind=engine)

@app.get("/")
def HomePage():
    return get_swagger_ui_html(openapi_url="openapi.json", title="Home_Page")


if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 8000, reload=True)
