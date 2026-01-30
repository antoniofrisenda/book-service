from fastapi import FastAPI
from pkg.config.mogodb import get_mongoDb
from pkg.controller import book_controller, reservation_controller

connection = get_mongoDb()

app = FastAPI(
    
        title="Book-Service API",
        version="1.0.0"
    )

app.include_router(book_controller.router)
app.include_router(reservation_controller.router)

