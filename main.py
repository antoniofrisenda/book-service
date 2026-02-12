from fastapi import FastAPI, Response, status
from pkg.config.logger import setup_logging
from pkg.controller import book_controller, reservation_controller

setup_logging()

app = FastAPI(
    
        title="Book-Service API",
        version="1.0.1"
    )

app.include_router(book_controller.router)
app.include_router(reservation_controller.router)

@app.get("/healthz")
def root(response: Response) -> None:
    response.status_code = status.HTTP_200_OK