from fastapi import FastAPI

from app.core.errors import register_error_handlers

app = FastAPI(title="Pawgress API")
register_error_handlers(app)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
