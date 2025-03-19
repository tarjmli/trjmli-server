from fastapi import FastAPI
import logging
import uvicorn
from api.routes import user
from api.routes import project
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
class LoggerMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        logger.info(f"Request from {scope['client'][0]}:{scope['client'][1]} for {scope['path']}")

        async def log_send(message):
            logger.debug(f"Sent {message}")
            await send(message)

        await self.app(scope, receive, log_send)


app.middleware("http")(LoggerMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.include_router(user.router , prefix="/api/v1/")
app.include_router(project.router, prefix="/api/v1/")




if __name__ == "__main__":
  
    uvicorn.run(app, host="0.0.0.0", port=8000)



