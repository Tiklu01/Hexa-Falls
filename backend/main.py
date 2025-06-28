from fastapi import FastAPI
from routes.upload_routes import router as upload_router
import utils.cloudinary_config  # auto-loads config

app = FastAPI()
app.include_router(upload_router)
