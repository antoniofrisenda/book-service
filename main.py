from fastapi import FastAPI
import uvicorn
from pkg.controller import book_controller, reservation_controller

app = FastAPI(
    
        title="Book-Service API",
        version="1.0.1"
    )

app.include_router(book_controller.router)
app.include_router(reservation_controller.router)