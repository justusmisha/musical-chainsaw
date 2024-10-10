import uvicorn
from fastapi import FastAPI
from logger import logger
from BotRouter.app.api.activity import activity_router
from BotRouter.app.api.school import classes_router, teachers_router

app = FastAPI()

app.include_router(activity_router, prefix="/activity")
app.include_router(classes_router, prefix="/class")
app.include_router(teachers_router, prefix="/teacher")
# app.include_router(payment_router, prefix="/api/v1/payment", tags=["Payment"])
# app.include_router(subscription_router, prefix="/api/v1/subscription", tags=["Subscription"])
# app.include_router(user_router, prefix="/api/v1/user", tags=["User"])


@app.on_event("startup")
async def startup_event():
    logger.info("Starting FastAPI app")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)