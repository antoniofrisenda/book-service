from fastapi import FastAPI
from pkg.config.logger import setup_loguru_logger
from pkg.controller import book_controller, reservation_controller

setup_loguru_logger()

app = FastAPI(
    
        title="Book-Service API",
        version="1.0.1"
    )

app.include_router(book_controller.router)
app.include_router(reservation_controller.router)