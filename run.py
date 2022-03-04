from app.main import app

if __name__ == "__main__":
    import uvicorn

    # noinspection PyTypeChecker
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, log_level="debug", reload=True)
