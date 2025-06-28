from fastapi import FastAPI
from routes.upload_routes import router as upload_router
from routes.auth_route import router as auth_router
import utils.cloudinary_config  # auto-loads config

app = FastAPI()
app.include_router(upload_router)
app.include_router(auth_router)