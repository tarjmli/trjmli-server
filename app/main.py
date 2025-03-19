from fastapi import FastAPI, Request
import logging
from sqlalchemy import Engine
import uvicorn
from api.routes import user, project
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from db.session import Base,engine
import models.user 
import models.project
app = FastAPI()

# Base.metadata.create_all(bind=engine)
print("database created")
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request from {request.client.host}:{request.client.port} for {request.url}")
        response = await call_next(request)
        return response


app.add_middleware(LoggerMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)


app.include_router(user.router, prefix="/api/v1")
app.include_router(project.router, prefix="/api/v1")

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
